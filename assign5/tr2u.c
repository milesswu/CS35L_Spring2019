#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>

void InputError() {
  write(2, "Error reading input!\n", 21);
  exit(1);
}

void OutputError()  {
  write(2, "Error writing output!\n", 22);
  exit(1);
}

void AllocationError() {
  write(2, "Error allocating memory!\n", 25);
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
    write(2, "Invalid number of operands!\n", 28);
    exit(1);
  }
  char* from = argv[1];
  char* to = argv[2];
  size_t fromSize = strlen(from);
  size_t toSize = strlen(to);
  if (fromSize != toSize) {
    write(2, "Operands are different lengths!\n", 32);
    exit(1);
  }
  for (size_t i = 0; from[i] != '\0'; i++) {
    if (strchr(from + i + 1, from[i]) != NULL) {
      write(2, "Duplicates in first operand!\n", 29);
      exit(1);
    }
  }
  
  char* input = (char*) malloc(sizeof(char));
  char curr[1];
  int i = 0;
  int readStatus;
  while (1) {
    readStatus = read(STDIN_FILENO, &curr, 1);
    if (readStatus == -1)
      InputError();
    if (readStatus == 0)
      break;
    input[i] = curr[0];
    char* temp = realloc(input, (i+2)*sizeof(char));
    if (temp == NULL) {
      free(input);
      AllocationError();
    }
    input = temp;
    i++;
    
    if (curr[0] == '\n') {
      input[i] = '\0';
      char* temp = realloc(input, (i+2)*sizeof(char));
      if (temp == NULL) {
	free(input);
	AllocationError();
      }
      input = temp;
      i++;
      interpretInput(input, from, to);
      write(1, input, i);
      input = NULL;
      input = (char*) malloc(sizeof(char));
      if (input == NULL) {
	free(input);
	AllocationError();
      }
      i = 0;
      continue;
    }
    
  }
  input[i] = '\0';
  char* temp = realloc(input, (i+2)*sizeof(char));
  if (temp == NULL) {
    free(input);
    AllocationError();
  }
  input = temp;
  i++;
  
  interpretInput(input, from, to);
  write(1, input, i);
  free(input);
  exit(0);
}
