/*****************************************/
/* Author  :  Eman Mohamed               */
/* Version :  V01                        */
/* Date    : 28 SEP 2020                 */
/*****************************************/
#ifndef STK_PRIVATE_H
#define STK_PRIVATE_H

typedef struct
{
	volatile u32 CTRL   ;
	volatile u32 LOAD  ;
	volatile u32 CURRENT   ;
}MSTK_Type;

#define     MSTK    ((MSTK_Type*)0xE000E010)


#define     MSTK_SRC_PIOSC_DIV_4          0
#define     MSTK_SRC_SYSTEM_CLOCK         1

#define     MSTK_SINGLE_INTERVAL    0
#define     MSTK_PERIOD_INTERVAL    1


#endif
