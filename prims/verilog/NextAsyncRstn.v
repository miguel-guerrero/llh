module NextAsyncRstn(clk, rstn, d, q);

parameter W=1;

input clk;
input rstn;
input [W-1:0] d;
output [W-1:0] q;

reg [W-1:0] q;

always @(posedge clk or negedge rstn) begin
    if (~rstn) begin
        q <= {W{1'b0}};
    end
    else begin
        q <= d;
    end
end

endmodule
