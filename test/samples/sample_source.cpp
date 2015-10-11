#include <iostream>

///sample globals here
int gA = 1;
bool gB = false;

/**
 * Supported method-format
 */
void funct1(){

}

/**
 * Supported method-format
 */
void funct2(int a){

}

/**
 * Supported method-format
 */
void
funct3(int a, int b)
{

}

/**
 * Supported method-format
 */
void func4(){ }

/**
 * Supported method-format
 */
int func5(){

return 1;

}

/**
 * Supported method-format
 */
string func6(string s)
{ return s; }

/**
 * Supported method-format
 */
char
func7(){

return NULL;
}

/**
 * Supported method-format
 */
char*
func11(){

return NULL;
}

/***************************************************************/
/**
 * Not supported method-format
 */
void
func8
(
)
{
	///none
}

/**
 * Not supported method-format
 */
void
func9
()
{
	///none
}

/**
 * Not supported method-format
 */
void func10()
{
for(;;)
{
	//infinity
}
}


