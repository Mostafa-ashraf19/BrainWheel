/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 10 Decemeber 2020                        */
/* Version: V01                                      */
/*****************************************************/
# ifndef 	GDIO_INTERFACE_H
#define     GDIO_INTERFACE_H

#define GPIOA 0
#define GPIOB 1
#define GPIOC 2
#define GPIOD 3
#define GPIOE 4
#define GPIOF 5	

#define GPIOA_APB 6
#define GPIOB_APB 7
#define GPIOC_APB 8
#define GPIOD_APB 9
#define GPIOE_APB 10
#define GPIOF_APB 11


	

#define  INPUT 	     0
#define	 OUTPUT			 1

#define PULL_UP 	 0
#define PULL_DOWN 	 1



#define GPIO_HIGH 1
#define GPIO_LOW  0

            /* PINS DECLERATION */
#define PIN0   0
#define PIN1   1
#define PIN2   2
#define PIN3   3
#define PIN4   4
#define PIN5   5
#define PIN6   6
#define PIN7   7
#define PIN8   8
#define PIN9   9
#define PIN10  10
#define PIN11  11
#define PIN12  12
#define PIN13  13
#define PIN14  14
#define PIN15  15

			/*  Functions Prototypes */
void MGPIO_voidInit (u8 copy_u8PORT);

void MGPIO_voidSetPinDirection (u8 copy_u8PORT,u8 copy_u8PIN, u8 copy_u8Mode  ) ;

void MGPIO_voidSetPinValue (u8 copy_u8PORT,u8 copy_u8PIN, u8 copy_u8Value);

u8 MGPIO_voidGETPinValue (u8 copy_u8PORT,u8 copy_u8PIN);





#endif
