module tb;

reg clk;
reg rstn;
wire inc=1;
wire [3:0] cnt;


initial begin
    $dumpfile ("dump.vcd");
    $dumpvars(0);
end

initial begin
    rstn <= 0;
    #10;
    rstn <= 1;
end

initial begin: clock_gen
    integer i;
    for (i=0; i<20; i=i+1) begin
        clk <= 0;
        #50;
        clk <= 1;
        #50;
    end
    $finish;
end

initial begin: mon
    integer exp;
    exp = 1;
    @(negedge clk)
    forever begin
        @(negedge clk)
        $display($time, " cnt ", cnt);
        if (exp != cnt) begin
            $display("missmatch exp=", exp, "cnt=", cnt);
            $finish;
        end
        exp = (exp + 1) & 4'hF;
    end
end

Counter4 i_counter4_0 (
    .clk(clk),
    .rstn(rstn),
    .inc(inc),
    .cnt(cnt)
);

endmodule
