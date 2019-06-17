#include <stdio.h>
#include <stdlib.h>

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

int compar(const void * a, const void * b) {
  return frobcmp(*(char**) a, *(char**) b);
}

void checkInput() {
  if (ferror(stdin) != 0) {
    fprintf(stderr, "Error reading input!");
    exit(1);
  }
}

void checkOutput() {
  if (ferror(stdout) != 0) {
    fprintf(stderr, "Error reading output!");
    exit(1);
  }
}

void AllocationError() {
  fprintf(stderr, "Error while allocating memory!");
  exit(1);
}

int main() {
  char* currWord = (char*) malloc(sizeof(char));
  char** allWords = (char**) malloc(sizeof(char*));
  char curr;
  int charIt = 0;
  int wordIt = 0;
  while (curr != EOF)
  {
    curr = getchar();
    checkInput();
    if (curr == EOF && charIt != 0) {
      currWord[charIt] = ' ';
    }
    else
      currWord[charIt] = curr;
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
    } else {
      char* tempWord = (char*) realloc(currWord, (charIt+2) * sizeof(char));
      if (tempWord == NULL) {
	printf("%s", "ever");
	free(currWord);
	free(allWords);
	AllocationError();
      }
      currWord = tempWord;
      charIt++;
    }
  }
  
  qsort(allWords, wordIt, sizeof(char*), compar);
  printf("%d\n", wordIt);
  unsigned long i;
  unsigned long j;
  for (i = 0; i < wordIt; i++) {
    for (j = 0; ;j++) {
      putchar(allWords[i][j]);
      checkOutput();
      if (allWords[i][j] == ' ') {
	break;
      }
    }
  }
  free(currWord);
  free(allWords);
}
