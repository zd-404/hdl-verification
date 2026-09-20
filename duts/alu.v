`timescale 1ns / 1ps

module alu (
    input  [7:0] a,          // الرقم الأول
    input  [7:0] b,          // الرقم الثاني
    input  [2:0] op,         // العملية (3 بت = 8 عمليات)
    output reg [7:0] result, // النتيجة
    output reg zero          // علم: النتيجة صفر؟
);

    // رموز العمليات
    localparam ADD = 3'b000;
    localparam SUB = 3'b001;
    localparam AND = 3'b010;
    localparam OR  = 3'b011;
    localparam XOR = 3'b100;
    localparam NOT = 3'b101;
    localparam SHL = 3'b110;
    localparam SHR = 3'b111;

    always @(*) begin
        case (op)
            ADD: result = a + b;
            SUB: result = a - b;
            AND: result = a & b;
            OR:  result = a | b;
            XOR: result = a ^ b;
            NOT: result = ~a;
            SHL: result = a << 1;
            SHR: result = a >> 1;
            default: result = 8'b00000000;
        endcase

        // علم الصفر: إذا النتيجة 0، العلم يرتفع
        zero = (result == 8'b0);
    end

endmodule