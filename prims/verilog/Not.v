module Not(a, z);

parameter W=1;

input [W-1:0] a;
output [W-1:0] z;

assign z = ~a;

endmodule
