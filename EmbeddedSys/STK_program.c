/*****************************************/
/* Author  :  Eman Mohamed               */
/* Version :  V01                        */
/* Date    : 28 SEP 2020                 */
/*****************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "STK_interface.h"
#include "STK_private.h"
#include "STK_config.h"


/* Define Callback Global Variable */
static void(*MSTK_CallBack)(void);

/* Define Variable for interval mode */
static u8 MSTK_u8ModeOfInterval;

void MSTK_voidInit(void)
{
//#if MSTK_CLK_SRC == MSTK_SRC_SYSTEM_CLOCK
    /* Disable STK - Disable STK Interrupt - Set clock source SYSTEM_CLOCK */
		 	MSTK -> CTRL = 0x00000004;
//#else
    /* Disable STK - Disable STK Interrupt - Set clock source PIOSC_DIV_4  */
	//MSTK -> CTRL = 0;
	
//#endif
}

void MSTK_voidSetBusyWait( u32 Copy_u32Ticks )
{
	/* Load ticks to load register */
	MSTK -> LOAD = Copy_u32Ticks;
	MSTK -> CURRENT = 0;
	
	/* Enable SysTick Timer */
	SET_BIT(MSTK->CTRL, 0);
	
	/* Wait till flag is raised */
	while( (GET_BIT(MSTK->CTRL,16)) == 0);
	
	/* Stop Timer */
	CLR_BIT(MSTK->CTRL, 0);
	MSTK -> LOAD = 0;
	MSTK -> CURRENT  = 0;
	
}
// avialable only with 16MHZ clock && max value is 1000ms to avoid overflow
void MSTK_voidDelay_ms( u32 Copy_u32mSec )
{
	/* Load ticks to load register */
	MSTK -> LOAD = Copy_u32mSec * (16000)-1;
	
	/* Start Timer */
	SET_BIT(MSTK->CTRL, 0);
	
	/* Wait till flag is raised */
	while( (GET_BIT(MSTK->CTRL,16)) == 0);
	
	/* Stop Timer */
	SET_BIT(MSTK->CTRL, 0);
	MSTK -> LOAD = 0;
	MSTK -> CURRENT  = 0;
	
}

void MSTK_voidSetIntervalSingle  ( u32 Copy_u32Ticks, void (*Copy_ptr)(void) )
{
	/* Load ticks to load register */
	MSTK -> LOAD = Copy_u32Ticks;
	
	/* Start Timer */
	SET_BIT(MSTK->CTRL, 0);
	
	/* Save CallBack */
	MSTK_CallBack = Copy_ptr;
	
	/* Set Mode to Single */
	MSTK_u8ModeOfInterval = MSTK_SINGLE_INTERVAL;
	
	/* Enable STK Interrupt */
	SET_BIT(MSTK->CTRL, 1);
}

void MSTK_voidSetIntervalPeriodic( u32 Copy_u32Ticks, void (*Copy_ptr)(void) )
{
	/* Load ticks to load register */
	MSTK -> LOAD = Copy_u32Ticks;
	
	/* Start Timer */
	SET_BIT(MSTK->CTRL, 0);
	
	/* Save CallBack */
	MSTK_CallBack = Copy_ptr;
	
	/* Set Mode to Single */
	MSTK_u8ModeOfInterval = MSTK_PERIOD_INTERVAL;
	
	/* Enable STK Interrupt */
	SET_BIT(MSTK->CTRL, 1);
}

void MSTK_voidStopInterval(void)
{
	/* Disable STK Interrupt */
	CLR_BIT(MSTK->CTRL, 1);
	
	/* Stop Timer */
	SET_BIT(MSTK->CTRL, 0);
	MSTK -> LOAD = 0;
	MSTK -> CURRENT  = 0;
}

u32  MSTK_u32GetElapsedTime(void)
{
	u32 Local_u32ElapsedTime;
	
	Local_u32ElapsedTime = MSTK -> LOAD - MSTK -> CURRENT ;
	
	return Local_u32ElapsedTime;
}

u32  MSTK_u32GetRemainingTime(void)
{
	u32 Local_u32RemainTime;
	
	Local_u32RemainTime = MSTK -> CURRENT ;
	
	return Local_u32RemainTime;
}

void SysTick_Handler(void)
{
	u8 Local_u8Temporary;
	
	if (MSTK_u8ModeOfInterval == MSTK_SINGLE_INTERVAL)
	{
		/* Disable STK Interrupt */
		CLR_BIT(MSTK->CTRL, 1);
	
		/* Stop Timer */
		SET_BIT(MSTK->CTRL, 0);
		MSTK -> LOAD = 0;
		MSTK -> CURRENT  = 0;
	}
	
	/* Callback notification */
	MSTK_CallBack();
	
	/* Clear interrupt flag By read it*/
	Local_u8Temporary = GET_BIT(MSTK->CTRL,16);
}
