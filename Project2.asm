# PART A
addi $8, $0, 3 # initial seed
addi $9, $0, 16 # numS = 16
addi $10,$0, 0 # increment address by 4 bytes
addi $13, $0, 0 # ctr = 0
addu $14, $0, $8 # tempS = seed
addu $11, $0, 0x000000FF # 00...0011111111
addu $17, $0, 0xFF000000 # 1111111100...00
addu $18, $0, 0x0000FFFF # 00...1111111111111111

do_loop: 	addi $12, $0, 0 # i = 0
		sw $14, 0x2010($10) # store value $14 into mem address

	for_loop:	addi $15, $8, -1 # seed - 1	
			slt $16, $12, $15 # i < seed - 1?
			beq $16, $0, for_end # if $16 = 0 jump to for_end
			addu $14, $14, $8 # tempS += seed, add current number n - 1 times
			addi $12, $12, 1 # i++
			beq $0, $0, for_loop
			#j for_loop
	
	for_end:	addi $13, $13, 1 # ctr++		
			addi $10, $10, 4 # increment address incrementer by 4 
			and $12, $14, $11 # preserves right most bits
			and $15, $14, $17 # preserves left most bits
			srl $15, $15, 16 # position left most bits into the right places i.e. 16...9
			addu $14, $15, $12 # merge both left and right most bits
			and $14, $14, $18 # sign extend to 0 
			addu $8, $0, $14 # seed = new 16 bit number
	
slt $16, $13, $9 # ctr < numS
bne $16,$0, do_loop # if $16 != 0 jump to do_loop 

#################################################################
#PART B i.

addi $9, $0, 0x2010 # point to first address
addi $10, $0, 0 # sum = 0
addi $14, $0, 16 # numS = 16
addi $11, $0, 0 # ctr = 0

do_avgHam1:	lw $8, ($9) # load value in current mem address 
		addi $12, $0, 0 # i = 0 
	
do_avgHam2:	slt $16, $8, $0 # $8 value < 0?
		beq $16, $0, skip # if $16 = 0 jump to skip
		addi $12, $12, 1 # i++ when $8 is negative
	skip:	sll $8, $8, 1 # logic shift to the left once until all 1's are gone
		bne $8, $0, do_avgHam2 # while($8 != 0)
		add $10, $10, $12 # sum of 1's in all 16 seeds, Hamming weight
		addi $14, $14, -1 # decrement numS for each iteration by 1
		addi $9, $9, 4 # increment address incrementer by 4
	
bne $14, $0, do_avgHam1 # if $14 != 0 jump to do_avgHam1

srl $11, $10, 4 # Average Hamming Weight
sw $11, 0x2000 # store AHW in address 0x2000

#################################################################
#PART B ii.

addi $10, $0, 0x2010 # point to first address, first seed pointer
addi $11, $0, 4 # second seed incrementer
addi $14, $0, 15 # numS = 15
addi $12, $0, 0 # sum = 0

do_avgDisHam1:	addi $13, $0, 0 # i = 0 
		lw $8, ($10) # load value from first seed pointer
		lw $9, 0x2010($11) # load value from second seed pointer

		xor $15, $8, $9 # make a new number from the different bits between values

	 # loop from s0 ... s14
	do_avgDisHam2:	slt $16, $15, $0 # $8 value < 0?
			beq $16, $0, skip2 # if $16 = 0 jump to skip
			addi $13, $13, 1 # i++ when $15 is negative, counts the 1s
			skip2:	sll $15, $15, 1 # logic shift to the left once until all 1's are gone
			bne $15, $0, do_avgDisHam2 # while($15 != 0)
			
		add $12, $12, $13 # sum of bit differences in all 15 seeds
		addi $14, $14, -1 # decrement numS for each iteration by 1
		addi $10, $10, 4 # increment address incrementer by 4
		addi $11, $11, 4 # increment address incrementer by 4
	
bne $14, $0, do_avgDisHam1 # if $14 != 0 jump to do_avgHam1

# determine the hamming distance between s15 and s0
addi $11, $0, 0 # set second seed incrementer to 0
lw $8, ($10) # load value in current mem address 
lw $9, 0x2010($11) # load value in the first mem address

xor $15, $8, $9 # make a new number from the different bits between values
addi $13, $0, 0 # i = 0 

do_avgDisHam3: slt $16, $15, $0 # $8 value < 0?
		beq $16, $0, skip3 # if $16 = 0 jump to skip
		addi $13, $13, 1 # i++ when $15 is negative, counts the 1s
	skip3:	sll $15, $15, 1 # logic shift to the left once until all 1's are gone

bne $15, $0, do_avgDisHam3 # while($15 != 0)
	
add $12, $12, $13 # sum of bit differences in all 16 seeds
srl $11, $12, 4 # Average Hamming Distance
sw $11, 0x2004 # store AHW in address 0x2000
