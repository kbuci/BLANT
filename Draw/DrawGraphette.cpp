#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <algorithm>
//Requires c++11 for stoull
#include <string>
#include <vector>
#include <cstring>
#include <cstdio>
#include <math.h>
#include <unistd.h>
#include "graphette2dotutils.h"

using std::cout;
using std::cerr;
using std::string;
using std::stringstream;
using std::ofstream;
using std::ifstream;
using std::vector;

void parseInput(int argc, char* argv[], int& k, vector<string>& inputBitstrings, string& outputFile, string& namesFile, bool& isUpper, string& graphTitle, int& edgewidth);
void printUsage();
void printHelp();
string toBitString(unsigned long long inputDecimalNum, int k);
string appendLeadingZeros(const string& inputBitstring, int k);

void createDotfileFromBit(int k, const vector<string>& inputBitstring, const string& outputFile, const string& namesFile, bool isUpper, const string& graphTitle, int edgewidth);
string getPos(int i, int k);
void writeEdges(ofstream& outfile, const vector<string>& inputBitstrings, int k, bool isUpper, int edgewidth);
void writeEdgesUpper(ofstream& outfile, const vector<string>& inputBitstrings, int k, int edgewidth);
void writeEdgesLower(ofstream& outfile, const vector<string>& inputBitstrings, int k, int edgewidth);
void printGraphConversionInstruction(const string& fileName);

//Functions from libwayne and libblant.c
extern "C" {
	struct SET;
	SET *SetAlloc(unsigned int n);
    int canonListPopulate(char *BUF, int *canon_list, SET *connectedCanonicals, int k);
}

const int RADIUS_SCALING = 25;
const string USAGE = "USAGE: graphette2dot <-k number_of_nodes> <-b bitstring | -d decimal_representation | -i lower_ordinal> <-o output_filename> [-n input_filename] [-u | -l] [-t title] [-e edge width] -h for verbose help\n";
const string NODE_ARGS = "shape = \"none\", fontsize = 24.0";
const string TITLE_ARGS = "fontsize = 24.0";
const string DECIMAL_INPUT_WARNING = "Warning. Decimal input was used with k > 11. Edge information may have been lost.\n";
const double PI  =3.141592653589793238463;
const vector<string> COLORS = {"black", "red", "lawngreen", "orange", "blue", "yellow", "indigo"};
const int DEFAULT_EDGE_WIDTH = 1;

int main(int argc, char* argv[]) {
	int k = 0;
	vector<string> inputBitstrings;
	string outputFile = "", namesFile = "", graphTitle = "";
	int edgewidth = DEFAULT_EDGE_WIDTH;
	//Defaults to lower row major bitstring/decimal interpretation
	bool isUpper = false;

	//Parses input passing variables by reference.
	parseInput(argc, argv, k, inputBitstrings, outputFile, namesFile, isUpper, graphTitle, edgewidth);

	createDotfileFromBit(k, inputBitstrings, outputFile, namesFile, isUpper, graphTitle, edgewidth);

	printGraphConversionInstruction(outputFile);

	return EXIT_SUCCESS;
}

/**
 * Parses command line input.
 * Doesn't allow for repeated inputs.
 * Prints usage and exits if invalid input is passed.
 * */
void parseInput(int argc, char* argv[], int& k, vector<string>& inputBitstrings, string& outputFile, string& namesFile, bool& isUpper, string& graphTitle, int& edgewidth) {
	bool input = false, matrixType = false;
	unsigned long long inputDecimalNum = 0;
	int opt;
	vector<unsigned long long> ordinals;

	while((opt = getopt(argc, argv, "k:b:d:i:o:t:e:nhul")) != -1)
    {
		switch(opt)
		{
		case 'k':
			if (k > 0) {
				cerr << "Only one k is allowed\n";
				printUsage();
			}
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			k = atoi(optarg);
			break;

		case 'b':
			input = true;
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			inputBitstrings.push_back(optarg);
			break;

		case 'd':
			input = true;
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			inputDecimalNum = std::stoull(optarg);
			inputBitstrings.push_back(toBitString(inputDecimalNum, k));

			if (k > 11)
				cerr << DECIMAL_INPUT_WARNING;
			break;

		case 'i':
			input = true;
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			ordinals.push_back(std::stoull(optarg));
			break;

		case 'o':
			if (!outputFile.empty()) {
				cerr << "Only one output file is allowed.\n";
				printUsage();
			}
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			outputFile = optarg;
			break;

		case 't':
			if (!graphTitle.empty()) {
				cerr << "Only one title allowed.\n";
				printUsage();
			}
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			graphTitle = optarg;
			break;

		case 'e':
			if (edgewidth != DEFAULT_EDGE_WIDTH) {
				cerr << "Only one edge width allowed.\n";
				printUsage();
			}
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			edgewidth = atoi(optarg);
			break;
		case 'n':
			if (!namesFile.empty()) {
				cerr << "Only one names file is allowed.\n";
				printUsage();
			}
			if (!*(optarg)) {
				cerr << "No following argument to " << opt << '\n';
				printUsage();
			}
			namesFile = optarg;
			break;

		case 'h':
			printHelp();
			break;

		case 'u':
			if (matrixType) {
				cerr << "Only one matrix type allowed.\n";
				printUsage();
			}
			isUpper = true;
			matrixType = true;
			break;

		case 'l':
			if (matrixType) {
				cerr << "Only one matrix type allowed.\n";
				printUsage();
			}
			isUpper = false;
			matrixType = true;
			break;

		default:
			cerr << "Unrecognized argument: " << opt << "\n";
			printUsage();
		}
	}

	//Check if k, input data, and output file were selected
	if (!(k > 0 && input && outputFile.size() > 0))
		printUsage();

	if (!ordinals.empty()) {
		if (k < 3 || k > 8) {
			cerr << "Ordinal input is only allowed for k between 3 and 8 (inclusive)\n";
			exit(EXIT_FAILURE);
		}
		isUpper = false;
		char BUF[BUFSIZ];
		int _canonList[12346];
		unsigned _Bk = (1 <<(k*(k-1)/2));
		SET *_connectedCanonicals = SetAlloc(_Bk);
		int _numCanon = canonListPopulate(BUF, _canonList, _connectedCanonicals, k);
		for (auto ordinal : ordinals) {
			if (ordinal < 0 || ordinal > _numCanon) {
				cerr << "Ordinal for k: " << k << " must be between 0 and " << _numCanon << '\n';
				exit(EXIT_FAILURE);
			}
			inputBitstrings.push_back(toBitString(_canonList[ordinal], k));
		}
	}

	for (string& bitstring : inputBitstrings) {
		bitstring = appendLeadingZeros(bitstring, k);
	}
}

void printUsage() {
	cerr << USAGE;
	exit(EXIT_SUCCESS);
}

//Contains useful information about the assumptions made in the program.
void printHelp() {
	std::cout << USAGE 
			  << "You must specify the number of nodes with -k\n"
			  << "Currently number of nodes is limited to 11 if decimal input is used\n"
			  << "This is because k=12 requires 66 bits to store the decimal input\n"
			  << "You must specify at least one bitstring, decimal, or ordinal input with -b -d or -i respectively\n"
			  << "-u and -l specify if all input is upper or lower triangular row major. Lower is assumed for ordinal input.\n"
			  << "Lower triangular row major is assumed\n"
			  << "You must specify an output file name with -o\n"
			  << "Please do not include file extension for output. The program with generate a .dot\n"
			  << "If no names file is selected, nodes will be named 0, 1, ...., (k-1)\n"
			  << "Names file parsing assumes one name per line\n"
			  << "You may specify a title with -t\n"
			  << "You may specify an edge width with -e. 1 is default\n"
			  << "If less names than nodes, additional nodes will be labeled by their index #\n"
			  << "If more names than nodes, additional names will be ignored\n";
	exit(EXIT_SUCCESS);
}

/**Creates .dot file from given input.
 * First, node names are listed.
 * If a names file was specified, the nodes are labeled with their name.
 * If the names file has a different number of names than k,
 * extra names become isolated nodes and additional nodes aren't labeled.
 * Then the edges are written to the file.
 * */
void createDotfileFromBit(int k, const vector<string>& inputBitstrings, const string& outputFile, const string& namesFile, bool isUpper, const string& graphTitle, int edgewidth) {
	int finalBitstringSize = (k * (k - 1)) / 2;
	int size;
	for (string inputBitstring : inputBitstrings) {
		size = inputBitstring.size();
		if (finalBitstringSize != size) {
			cerr << "Input size does not match number of nodes.\n"
				<< "Expected Bitstring Size given k = " << k << " is:  "
				<< finalBitstringSize << "\nInput Bitstring Size: " << size << "\n";
			exit(EXIT_FAILURE);
		}
	}

	ofstream outfile;
	stringstream ss;
	ss << outputFile << ".dot";
	outfile.open(ss.str());
	if (!outfile) {
		cerr << "Unable to create Dot File " << ss.str() << "\n";
		exit(EXIT_FAILURE);
	}
	
	outfile << "graph {\n";

	int i = 0;
	if (namesFile != "") {
		std::ifstream infile;
		infile.open(namesFile);
		if (infile) {
			string nodeName;
			while (std::getline(infile, nodeName) && i < k) {
				outfile << 'n' << i << " [label=\"" << nodeName << "\", pos=\"" << getPos(i, k) << "!\"" << NODE_ARGS << ";]\n";
				i++;
			}
			if (i < k) {
				cerr << "Warning: Less nodes in names file than -k.\n"
					 << "Number of nodes: " << k << " Names file number of nodes: " << i << "\n";
			}

			while (std::getline(infile, nodeName))
				i++;
			if (i > k) {
				cerr << "Warning: More nodes in names file than -k.\n"
			         << "Number of nodes: " << k << " Names file number of nodes: " << i << "\n";								
			}

			infile.close();
		} else {
			cerr << "Could not open name file\n";
		}
	}
	while (i < k) {
		outfile << 'n' << i << "[label=\"" << i << "\", pos=\"" << getPos(i, k) <<  "!\"" << NODE_ARGS << "]\n";
		i++;
	}

	writeEdges(outfile, inputBitstrings, k, isUpper, edgewidth);
	if (graphTitle != "") {
		outfile << "labelloc=\"b\";\n"
				<< "label=\"" << graphTitle << "\"\n"
				<< TITLE_ARGS << '\n';
	}
	outfile << "}";
	outfile.close();
}

string getPos(int i, int k) {
	stringstream ss;
	ss << RADIUS_SCALING * k * cos(PI /2 - (2 * PI / k * i)) << ", " << RADIUS_SCALING * k * sin(PI / 2 - (2 * PI / k * i));
	return ss.str();
}

//Wrapper function to choose edge writing function based on matrix representation.
void writeEdges(ofstream& outfile, const vector<string>& inputBitstrings, int k, bool isUpper, int edgewidth) {
	if (isUpper)
		writeEdgesUpper(outfile, inputBitstrings, k, edgewidth);
	else
		writeEdgesLower(outfile, inputBitstrings, k, edgewidth);
}

//Assuming row major
void writeEdgesUpper(ofstream& outfile, const vector<string>& inputBitstrings, int k, int edgewidth) {
	size_t size = inputBitstrings[0].size();
	int i = 0, j = 1, color = 0;
	string penwidth = "";
	if (edgewidth != 1) {
		penwidth = (", penwidth=" + std::to_string(edgewidth));
	}
	for (size_t k = 0; k < size; k++) {
		//Look at every string if they have an edge
		color = 0;
		for (string inputBitstring : inputBitstrings) {
			if (inputBitstring[k] == '1')
				outfile << "n" << i << " -- " << "n" << j << "[color=" << COLORS[color] << penwidth << "]" << "\n";
			else if (inputBitstring[k] != '0')
				cerr << "Unknown input: " << inputBitstring[k] << " in input bitstring.\n";

			color++;
			if (color > static_cast<int>(COLORS.size())) {
				cerr << "Too many graphs: Add colors to colors array" << std::endl;
				exit(EXIT_FAILURE);
			}
		}

		//iterate through pretend adjecency matrix
		j++;
		if (j == k) {
			i++;
			j = i + 1;
		}
	}
}

//Assuming row major
void writeEdgesLower(ofstream& outfile, const vector<string>& inputBitstrings, int k, int edgewidth) {
	size_t size = inputBitstrings[0].size();
	unsigned int i = 1, j = 0, color = 0;
	string penwidth = "";
	if (edgewidth != 1) {
		penwidth = (", penwidth=" + std::to_string(edgewidth));
	}
	for (size_t k = 0; k < size; k++) {
		//Look at every string if they have an edge
		color = 0;
		for (string inputBitstring : inputBitstrings) {
			if (inputBitstring[k] == '1')
				outfile << "n" << i << " -- " << "n" << j << "[color=" << COLORS[color] << penwidth << "]" << "\n";
			else if (inputBitstring[k] != '0')
				cerr << "Unknown input: " << inputBitstring[k] << " in input bitstring.\n";

			color++;
		}

		//iterate through pretend adjecency matrix
		j++;
		if (j == i) {
			i++;
			j = 0;
		}
	}
}

void printGraphConversionInstruction(const string& filename) {
	stringstream ss;
	ss << "neato -n -Tpdf \"" << filename << ".dot\" -o \"" << filename << ".pdf\"";
	std::cout << ss.str() << std::endl;
}
