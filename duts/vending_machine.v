`timescale 1ns / 1ps

module vending_machine (
    input clk,
    input rst,
    input coin5,
    input coin10,
    input cancel,
    output reg dispense,
    output reg change5,
    output reg change10
);

    // تعريف الحالات
    localparam IDLE     = 3'b000;
    localparam FIVE     = 3'b001;
    localparam TEN      = 3'b010;
    localparam DISPENSE = 3'b011;
    localparam CANCEL   = 3'b100;

    reg [2:0] state, next_state;
    reg change5_next, change10_next;

    // 1. تحديث الحالة عند كل حافة ساعة
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
            change5 <= 0;
            change10 <= 0;
        end else begin
            state <= next_state;
            change5 <= change5_next;
            change10 <= change10_next;
        end
    end

    // 2. منطق الانتقال والمخارج
    always @(*) begin
        next_state = state;
        dispense = 0;
        change5_next = 0;
        change10_next = 0;

        case (state)
            IDLE: begin
                if (coin5)       next_state = FIVE;
                else if (coin10) next_state = TEN;
            end

            FIVE: begin
                if (coin5)       next_state = TEN;
                else if (coin10) next_state = DISPENSE;
                else if (cancel) begin next_state = CANCEL; change5_next = 1; end
            end

            TEN: begin
                if (coin5)       next_state = DISPENSE;
                else if (coin10) begin next_state = DISPENSE; change5_next = 1; end
                else if (cancel) begin next_state = CANCEL; change10_next = 1; end
            end

            DISPENSE: begin
                dispense = 1;
                next_state = IDLE;
            end

            CANCEL: begin
                next_state = IDLE;
            end

            default: next_state = IDLE;
        endcase
    end

endmodule