.data #they are dynamically allocated in the memory
    welcome: .asciiz "Hi, Welcome to KaalKoot. We provide encryption decryption services.\n"
    nameMessage: .asciiz "Please enter Your Name: "
    name: .space 50
    welcome2: .asciiz "Welcome "
    newLine: .asciiz "\n"
    encryptMessage: .asciiz "Please Enter the Message You Want to Encrypt: "
    decryptMessage: .asciiz "Please Enter the Message You Want to Decrypt: "
    optionMessage: .asciiz "\n Please Enter one of the below options: "
    option1: .asciiz "\n 0. Encrypt a Message"
    option2: .asciiz "\n 1. Decrypt a Message\n"
    enter: .asciiz "Enter: "
    message: .space 500   #.space is used in order to store the string input from the user
    output: .space 500

    outputMessage: .asciiz "Your output String is: "

#This program implements reverse ciphering
.text
    main:
        jal warming #To welcome the user

        la $a0, optionMessage  #Menu based program where the user can encrypt or decrypt
        jal printMessage

        la $a0, option1
        jal printMessage

        la $a0, option2
        jal printMessage

        la $a0, enter
        jal printMessage

        li $v0,5
        syscall
        move $t5,$v0

        addi $t1,$zero,1

        beq $t5, $t1, decrypt
        beq $t5, $zero, encrypt

        li $v0,10
        syscall
        
    warming: #Simple procedure to welcome the user
        la $a0, welcome
        addi $sp, $sp,-4  #storing the stack pointer in the stack for returning from this procedure back to the main
        sw $ra, 0($sp)

        jal printMessage

        la $a0, nameMessage
        jal printMessage

        li $v0, 8
        la $a0, name
        li $a1, 50
        syscall

        la $a0, welcome2
        jal printMessage

        la $a0, name
        jal printMessage

        la $a0, newLine
        jal printMessage

        lw $ra, 0($sp)  #normalizing the sp register again to initial value
        addi $sp,$sp,4

        jr $ra

    encrypt:  #encryption procedure to encrypt your string
        la $a0, encryptMessage
        jal printMessage

        li $v0, 8
        la $a0, message #taking input from the user
        li $a1, 500
        syscall

        j logic

    decrypt:  #decryption procedure to decrypt the string
        la $a0, decryptMessage
        jal printMessage

        li $v0, 8
        la $a0, message
        li $a1, 500
        syscall

        j logic

    logic:  #ciphering logic of the program
        la $a0, message
        la $a1, output

        while:
            lb $t0, 0($a0)
            beqz $t0, exit

            li $t1, 122
            addi $t2, $zero, 97

            bgt $t0, $t1, notLowercase
            blt $t0, $t2, notLowercase

            add $t3, $t2, $t1
            sub $t0, $t3, $t0

            sb $t0, 0($a1)
            addi $a0, $a0, 1
            addi $a1, $a1, 1

            j while

    notLowercase: #this handles cases from A-Z
        li $t1, 65
        addi $t2, $zero, 90
        bgt $t0, $t2, notUppercase
        blt $t0, $t1, notUppercase
        add $t3, $t2, $t1
        sub $t0, $t3, $t0
        sb $t0, 0($a1)
        addi $a0, $a0, 1
        addi $a1, $a1, 1
        j while

    notUppercase: #this handles all the special symbols
        sb $t0, 0($a1)
        addi $a0, $a0, 1
        addi $a1, $a1, 1
        j while

    exit:   #exit procedure is used to mark the end of the program and appends \0 to the end of the string. The final string is also printed out
        li $t0, 0
        sb $t0, ($a1)

        la $a0, outputMessage
        jal printMessage

        la $a0, output
        jal printMessage

        la $a0, newLine
        jal printMessage

        li $v0,10
        syscall

    printMessage:  #this is the print procedure which is used to print strings
        li $v0, 4
        syscall
        jr $ra