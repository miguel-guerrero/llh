module And(a, b, z);

parameter W=1;

input [W-1:0] a;
input [W-1:0] b;
output [W-1:0] z;

assign z = a & b;

endmodule
