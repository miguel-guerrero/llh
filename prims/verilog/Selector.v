module Selector(a, idx, z);

parameter W=2;
parameter L2W = $clog2(W);

input [W-1:0] a;
input [L2W-1:0] idx;
output [0:0] z;

assign z = a[idx];

endmodule
