// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@KBD
M=0
@SCREEN
D=A
@pos
M=D
@8191
D=A
@max
M=D
@SCREEN
D=M
@max
M=M+D

@INIT
0;JMP

(WHITE)
    @pos
    A=M
    M=0

    @pos
    M=M+1
    D=M

    @24575
    D=D-A

    @INIT
    D;JEQ

    @WHITE
    D;JNE

(BLACK)
    @pos
    A=M
    M=-1

    @pos
    M=M+1
    D=M

    @24575
    D=D-A

    @INIT
    D;JEQ

    @BLACK
    D;JNE

(INIT)
    @SCREEN
    D=A
    @pos
    M=D
    @KBD
    D=M
    @BLACK
    D;JNE
    @WHITE
    D;JEQ
