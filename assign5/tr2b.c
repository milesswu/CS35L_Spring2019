#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void checkInput() {
  if (ferror(stdin) != 0) {
    fprintf(stderr, "Error reading input!\n");
    exit(1);
  }
}

void checkOutput()  {
  if (ferror(stdout) != 0) {
    fprintf(stderr, "Error writing output!\n");
    exit(1);
  }
}

void AllocationError() {
  fprintf(stderr, "Error allocating memory!\n");
  exit(1);
}

void interpretInput(char* input, char* from, char* to) {
  size_t i = 0;
  while(input[i] != '\0') {
    for (size_t j = 0; from[j] != '\0'; j++) {
      if (input[i] == from[j]) {
	input[i] = to[j];
	break;
      }
    }
    i++;
  }

}

int main(int argc, char* argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Invalid number of operands!\n");
    exit(1);
  }
  char* from = argv[1];
  char* to = argv[2];
  size_t fromSize = strlen(from);
  size_t toSize = strlen(to);
  if (fromSize != toSize) {
    fprintf(stderr, "Operands are different lengths!\n");
    exit(1);
  }
  int used[255];
  for (size_t i = 0; from[i] != '\0'; i++) {
    if (used[(int)from[i]] == 1) {
      fprintf(stderr, "Duplicates in first operand!\n");
      exit(1);
    }
    used[(int)from[i]] = 1;
  }
  char* input = (char*) malloc(sizeof(char));
  char curr;
  int i = 0;
  while ((curr = getchar()) != EOF) {
    checkInput();
    if (curr == '\n') {
      interpretInput(input, from, to);
      printf("%s\n", input);
      checkOutput();
      input = NULL;
      input = (char*) malloc(sizeof(char));
      if (input == NULL) {
	free(input);
	AllocationError();
      }
      i = 0;
      continue;
    }
    input[i] = curr;
    char* temp = realloc(input, (i+2)*sizeof(char));
    if (temp == NULL) {
      free(input);
      AllocationError();
    }
    input = temp;
    i++;
  }
  
  input[i] = '\0';
  char* temp = realloc(input, (i+2)*sizeof(char));
  if (temp == NULL) {
    free(input);
    AllocationError();
  }
  input = temp;
  
  interpretInput(input, from, to);
  printf("%s", input);
  checkOutput();
  free(input);
  exit(0);
}
