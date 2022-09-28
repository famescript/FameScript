function main zero {
  a = 0;
  try {
   a = number(scanf("First Number : "));
   b = scanf("operator : ");
   c = number(scanf("second number : "));
   if (b == "+") {
    printf(a + c);
    printf("\n");
   };
   if (b == '-') {
    printf(a - c);
    printf("\n");
   };
   if (b == '/') {
    printf(a / c);
    printf("\n");
   };
   if (b == '*') {
    printf(a*c);
    printf("\n")
   };
   a = 1;
  };
  if (a == 0) {
    printf("Invaild Numbers")
    printf("\n");
  };
};
