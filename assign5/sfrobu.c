#include <stdio.h> //TODO: Remove this when done, should not need for nondebugging purposes
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>
#include <limits.h>
#include <errno.h>
#include <getopt.h>

int caseInsensitive;
int counter = 0;
int frobcmp( char const * a, char const * b) {
  if (*a == ' ' && *b == ' ')
    return 0;
  if (*a == ' ')
    return -1;
  if (*b == ' ')
    return 1;
  while ( *a != ' ' && *b != ' ') {
    char unfr1 = *a ^ 0x2A;
    char unfr2 = *b ^ 0x2A;
    if (caseInsensitive) {
      if ((int)unfr1 >= 0)
	unfr1 = toupper(unfr1);
      if ((int)unfr2 >= 0)
	unfr2 = toupper(unfr2);
    }
    if (unfr1 > unfr2 || *b == ' ')
      return 1;
    else if (unfr1 < unfr2 || *a == ' ')
      return -1;
    else {
      a++;
      b++;
    }
  }  
  return 0;
}

int compare(const void * a, const void * b) {
  return frobcmp(*(char**) a, *(char**) b);
}

void InputError() {
  write(2, "Error reading input!\n", 21);
  exit(1);
}

void OutputError() {
  write(2, "Error writing output!\n", 22);
  exit(1);
}

void AllocationError() {
  write(2, "Error while allocating memory!\n", 31);
  exit(1);
}

int main(int argc, char* argv[]) {
  caseInsensitive = 0;
  int o;
  opterr = 0;

  while ((o = getopt(argc, argv, "f")) != -1) {
    switch (o) {
    case 'f':
      caseInsensitive = 1;
      break;
    case '?':
      write(2, "Invalid option!\n" , 16);
      exit(1);
      break;
    default:
      break;
    }
  }

  if (argc > 2) {
    write(2, "Too many operands!\n", 19);
    exit(1);
  }

  int isFile = 0;
  struct stat finfo;
  if (fstat(0, &finfo) != -1) {
    if (S_ISREG(finfo.st_mode) != 0)
      isFile = 1;
  }
  
  char* currWord = (char*) malloc(sizeof(char));
  char** allWords = (char**) malloc(sizeof(char*));
  char curr[1];
  int charIt = 0;
  int wordIt = 0;
  int readStatus = 1;
  if (isFile && finfo.st_size != 0) {
    int fsize = finfo.st_size;
    char* buffer = (char*) malloc(fsize);
    readStatus = read(0, buffer, fsize);
    if (readStatus == -1)
      InputError();
    if (buffer[fsize-1] != ' ') {
      buffer[fsize] = ' ';
      char* temp = realloc(buffer, (fsize+2)*sizeof(char));
      if (temp == NULL) {
	free(currWord);
	free(allWords);
	AllocationError();
      }
      buffer = temp;
      fsize++;
    }
    int numWords = 0;
    for (int i = 0; i < fsize; i++) {
      if (buffer[i] == ' ') {
	numWords++;
      }
    }

    char** tempArr = (char**) realloc(allWords, sizeof(char*)*numWords);
    if (tempArr == NULL) {
      free(currWord);
      free(allWords);
      AllocationError();
    }
    allWords = tempArr;
    
    int j = 0;
    for (wordIt = 0; wordIt < numWords; wordIt++) {
      while(j < fsize) {
	char currChar = buffer[j];
       	currWord[charIt] = currChar;
	char* tempWord = realloc(currWord, (charIt+2) * sizeof(char));
	if (tempWord == NULL) {
	  free(currWord);
	  free(allWords);
	  AllocationError();
	}
	charIt++;
	j++;
	if (currChar == ' ') {
	  break;
	}
	if (j == fsize && currChar != ' ') {
	  currWord[charIt] = ' ';
	  char* tempWord = realloc(currWord, (charIt+2) * sizeof(char));
	  if (tempWord == NULL) {
	    free(currWord);
	    free(allWords);
	    AllocationError();
	  }
	}
      }
      
      allWords[wordIt] = currWord;      
      charIt = 0;
      currWord = NULL;
      currWord = (char*)malloc(sizeof(char));
      if (currWord == NULL) {
	free(currWord);
	free(allWords);
	AllocationError();
      }

    }
    free(buffer);
  }
  currWord = NULL;
  currWord = (char*) malloc(sizeof(char));
  if (currWord == NULL) {
	free(currWord);
	free(allWords);
	AllocationError();
  }

  //Continue reading for growing files
  lseek(0, 0, SEEK_CUR);
  while (1)
  {
    readStatus = read(0, curr, 1);
    if (readStatus == -1)
      InputError();

    //handle EOF
    if (readStatus == 0 && charIt != 0) {
      currWord[charIt] = ' ';
    }
    else {
      currWord[charIt] = curr[0];
    }
    //add word to array if encounter space byte
    if (currWord[charIt] == ' ') {
      allWords[wordIt] = currWord;
      char** tempArr = (char**) realloc(allWords, (wordIt+2) * sizeof(char*));
      if (tempArr == NULL) {
	free(currWord);
	free(allWords);
	AllocationError();
      }
      allWords = tempArr;
      wordIt++;
      charIt = 0;
      currWord = NULL;
      currWord = (char*) malloc(sizeof(char));
      if (currWord == NULL) {
	free(currWord);
	free(allWords);
	AllocationError();
      }
      continue;
    }
    
    //parse next character in current word
    char* tempWord = (char*) realloc(currWord, (charIt+2) * sizeof(char));
    if (tempWord == NULL) {
      free(currWord);
      free(allWords);
      AllocationError();
    }
    currWord = tempWord;
    charIt++;
    if (readStatus == 0)
      break;
  }
  
  qsort(allWords, wordIt, sizeof(char*), compare);

  int i;
  int j;
  int currSize = 0;
  for (i = 0; i < wordIt; i++) {
    for (j = 0; ;j++) {
      currSize++;
      if (allWords[i][j] == ' ') {
	break;
      }
    }
    write(1, allWords[i], currSize);
    currSize = 0;
  }
  free(currWord);
  free(allWords);
  //  printf("calls to compare: %d\n", counter);
}
