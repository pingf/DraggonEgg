DraggonEgg
==========


INTRO
-------
self-designed simple language with one compiler front for arm-v7m and a vm for x86,which are both implemented with python language~

Author: Fanchao-MENG,ZZU university.


How to run?

1.edit file test.de

2.run "python compile.py ", then test.deout is generated.

3.run "python vm.py "

Simplicity
--------------------
Hi,I'm not the so called coding guy,I can not understand the codes longer than 
thousands of lines...oops.....

so this compiler(actually the front-end) only contains 850 lines of python.
Inspired by PLY and mini-c.
However, the mini-c is a little complex for me,I want to make the compiler much easier.
so I just use the Visitor Pattern as mini-c used.
However, I choose the GCC's ARM-v7m assemble language, which is much simpler than x86's.
designed one simple language called Draggon, now it's much simpler than std C.
the processes of type checking, error detecting are not included in this demo version for the reason of simplicity.


the annotated assemble file will be generated, however, you need to write linker script-file and 
startup assemble code to let it run on stm32 or lm3s chips.
a simple virtual machine is implemented, you can use it to test on normal pc.
with the help of python, when you test codes with the vm, you can forget about 
the overflow problem.


Example of DraggonEgg(proto version)
------------------------------------

1.calculate the fibs~


	function tail(n,b1,b2,begin){ 
		if (n == begin){ 
			return b1 + b2;
		} 
		else { 
			return tail(n, b2, b1 + b2, begin + 1);
		}
	}
	function fib(x){
		if (x>2){
			return tail(x, 1, 1, 3); 
		}else{
			return 1;
		}
	}
	function main(){
		return fib(100);
	}

2.array with pointer-like processing


	function arr(x,n){
		t=x;
		t=t+n*4; 
		return t;
	}
	function main(){
		a=1;b=2;c=3;d=4;e=5;f=6;g=7;  
		s=arr(<a,2);
		s=>s*4;
		return >s;
	}

3.swap function


	function swap(a,b){  
	    t=>a;>a=>b;>b=t;
	    return 0;
	} 
	function main(){
	    a=1;b=2;c=3;d=4;e=5;f=6;g=7;  
	    swap(<e,<g);
	    return e;
	}