/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 10 Decemeber 2020                        */
/* Version: V01                                      */
/*****************************************************/
# ifndef 	GDIO_PRIVATE_H
#define     GDIO_PRIVATE_H
 /* Base address */
#define GPIOA_AHP_BASE_ADDRESS 		0x40004000
#define GPIOA_APB_BASE_ADDRESS 		0x40058000
#define GPIOB_AHP_BASE_ADDRESS 		0x40005000
#define GPIOB_APB_BASE_ADDRESS 		0x40059000
#define GPIOC_AHP_BASE_ADDRESS 		0x40006000
#define GPIOC_APB_BASE_ADDRESS 		0x4005A000
#define GPIOD_AHP_BASE_ADDRESS 		0x40007000
#define GPIOD_APB_BASE_ADDRESS 		0x4005B000
#define GPIOE_AHP_BASE_ADDRESS 		0x40024000
#define GPIOE_APB_BASE_ADDRESS 		0x4005C000
#define GPIOF_AHP_BASE_ADDRESS 		0x40025000
#define GPIOF_APB_BASE_ADDRESS 		0x4005D000

#define GPIO_LOCK_KEY           0x4C4F434B 

				/*Clock register */
#define RCGCGPIO    *((u32*) 0x400FE608)    // Connect Clock on Selected PORT
#define PRGPIO      *((u32*) 0x400FEA08)    // Read only register to check that the clock connected on a selected PORT



	           /* REDISTERS ADDRESSES FOR PORT A AHP*/
#define GPIOA_AHP_DATA				*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x3FC))   // GPIO Data Register
#define GPIOA_AHP_DIR				  *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x400))  //GPIO Direction Register 
#define GPIOA_AHP_AFSEL				*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x420))  //GPIO Alternative Function Select
#define GPIOA_AHP_ODR			  	*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOA_AHP_PUR			    *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOA_AHP_PDR				  *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOA_AHP_DEN				  *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOA_AHP_LOCK				*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOA_AHP_CR				  *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOA_AHP_AMSEL				*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOA_AHP_CTL				  *((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOA_AHP_ADCCTL			*((u32*)(GPIOA_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT A APB*/
#define GPIOA_APB_DATA				*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x3FC ))
#define GPIOA_APB_DIR			  	*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x400))
#define GPIOA_APB_AFSEL				*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x420))
#define GPIOA_APB_ODR			  	*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOA_APB_PUR			    *((u32*)(GPIOA_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOA_APB_PDR			  	*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOA_APB_DEN				  *((u32*)(GPIOA_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOA_APB_LOCK				*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x520))  //GPIO Lock

#define GPIOA_APB_AMSEL				*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOA_APB_CTL				  *((u32*)(GPIOA_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOA_APB_ADCCTL			*((u32*)(GPIOA_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control


	           /* REDISTERS ADDRESSES FOR PORT B AHP*/
#define GPIOB_AHP_DATA				*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x3FC))
#define GPIOB_AHP_DIR				  *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x400))
#define GPIOB_AHP_AFSEL				*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x420))
#define GPIOB_AHP_ODR				  *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOB_AHP_PUR			    *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOB_AHP_PDR				  *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOB_AHP_DEN				  *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOB_AHP_LOCK				*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOB_AHP_CR				  *((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOB_AHP_AMSEL				*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOB_AHP_CTL			  	*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOB_AHP_ADCCTL			*((u32*)(GPIOB_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT B APB*/
#define GPIOB_APB_DATA				*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x3FC ))
#define GPIOB_APB_DIR			  	*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x400))
#define GPIOB_APB_AFSEL				*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x420))
#define GPIOB_APB_ODR			  	*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOB_APB_PUR			    *((u32*)(GPIOB_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOB_APB_PDR			  	*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOB_APB_DEN				  *((u32*)(GPIOB_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOB_APB_LOCK				*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOB_APB_AMSEL				*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOB_APB_CTL				  *((u32*)(GPIOB_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOB_APB_ADCCTL			*((u32*)(GPIOB_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control


	           /* REDISTERS ADDRESSES FOR PORT C AHP*/
#define GPIOC_AHP_DATA				*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x3FC))
#define GPIOC_AHP_DIR				  *((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x400))
#define GPIOC_AHP_AFSEL				*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x420))
#define GPIOC_AHP_ODR			  	*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOC_AHP_PUR			    *((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOC_AHP_PDR			  	*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOC_AHP_DEN				  *((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOC_AHP_LOCK				*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOC_AHP_CR				  *((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOC_AHP_AMSEL				*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOC_AHP_CTL				  *((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOC_AHP_ADCCTL			*((u32*)(GPIOC_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT C APB*/
#define GPIOC_APB_DATA				*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x3FC ))
#define GPIOC_APB_DIR			  	*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x400))
#define GPIOC_APB_AFSEL				*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x420))
#define GPIOC_APB_ODR				  *((u32*)(GPIOC_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOC_APB_PUR			    *((u32*)(GPIOC_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOC_APB_PDR				  *((u32*)(GPIOC_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOC_APB_DEN			  	*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOC_APB_LOCK				*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOC_APB_AMSEL				*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOC_APB_CTL				  *((u32*)(GPIOC_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOC_APB_ADCCTL			*((u32*)(GPIOC_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control


	           /* REDISTERS ADDRESSES FOR PORT D AHP*/
#define GPIOD_AHP_DATA				*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x3FC))
#define GPIOD_AHP_DIR			  	*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x400))
#define GPIOD_AHP_AFSEL				*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x420))
#define GPIOD_AHP_ODR				  *((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOD_AHP_PUR			    *((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOD_AHP_PDR			  	*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOD_AHP_DEN				  *((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOD_AHP_LOCK			 	*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOD_AHP_CR				  *((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOD_AHP_AMSEL				*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOD_AHP_CTL			   	*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOD_AHP_ADCCTL			*((u32*)(GPIOD_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT D APB*/
#define GPIOD_APB_DATA				*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x3FC ))
#define GPIOD_APB_DIR			  	*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x400))
#define GPIOD_APB_AFSEL				*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x420))
#define GPIOD_APB_ODR				  *((u32*)(GPIOD_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOD_APB_PUR			    *((u32*)(GPIOD_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOD_APB_PDR				  *((u32*)(GPIOD_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOD_APB_DEN				  *((u32*)(GPIOD_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOD_APB_LOCK				*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOD_APB_AMSEL				*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOD_APB_CTL				  *((u32*)(GPIOD_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOD_APB_ADCCTL			*((u32*)(GPIOD_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control


	           /* REDISTERS ADDRESSES FOR PORT E AHP*/
#define GPIOE_AHP_DATA				*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x3FC))
#define GPIOE_AHP_DIR			  	*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x400))
#define GPIOE_AHP_AFSEL				*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x420))
#define GPIOE_AHP_ODR				  *((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOE_AHP_PUR			    *((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOE_AHP_PDR			  	*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOE_AHP_DEN				  *((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOE_AHP_LOCK				*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOE_AHP_CR				  *((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOE_AHP_AMSEL			 	*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOE_AHP_CTL				  *((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOE_AHP_ADCCTL			*((u32*)(GPIOE_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT E APB*/
#define GPIOE_APB_DATA				*((u32*)(GPIOE_APB_BASE_ADDRESS + 0x3FC ))
#define GPIOE_APB_DIR				  *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x400))
#define GPIOE_APB_AFSEL				*((u32*)(GPIOE_APB_BASE_ADDRESS + 0x420))
#define GPIOE_APB_ODR				  *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOE_APB_PUR			    *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOE_APB_PDR				  *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOE_APB_DEN				  *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOE_APB_LOCK				*((u32*)(GPIOE_APB_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOE_APB_AMSEL				*((u32*)(GPIOE_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOE_APB_CTL				  *((u32*)(GPIOE_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOE_APB_ADCCTL			*((u32*)(GPIOE_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control


	           /* REDISTERS ADDRESSES FOR PORT F AHP*/
#define GPIOF_AHP_DATA				*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x3FC))
#define GPIOF_AHP_DIR			  	*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x400))
#define GPIOF_AHP_AFSEL				*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x420))
#define GPIOF_AHP_ODR				  *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOF_AHP_PUR			    *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOF_AHP_PDR				  *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOF_AHP_DEN				  *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOF_AHP_LOCK				*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOF_AHP_CR				  *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x524))  //GPIO Lock
#define GPIOF_AHP_AMSEL				*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOF_AHP_CTL				  *((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOF_AHP_ADCCTL			*((u32*)(GPIOF_AHP_BASE_ADDRESS + 0x530))  //GPIO ADC Control

	           /* REDISTERS ADDRESSES FOR PORT F APB*/
#define GPIOF_APB_DATA				*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x3FC))
#define GPIOF_APB_DIR			  	*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x400))
#define GPIOF_APB_AFSEL				*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x420))
#define GPIOF_APB_ODR				  *((u32*)(GPIOF_APB_BASE_ADDRESS + 0x50C))  //GPIO Open Drain Select
#define GPIOF_APB_PUR			    *((u32*)(GPIOF_APB_BASE_ADDRESS + 0x510))  //GPIO Pull-Up Select
#define GPIOF_APB_PDR				  *((u32*)(GPIOF_APB_BASE_ADDRESS + 0x514))  //GPIO Pull-Down Select
#define GPIOF_APB_DEN				  *((u32*)(GPIOF_APB_BASE_ADDRESS + 0x51C))  //GPIO Digital Enable
#define GPIOF_APB_LOCK				*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x520))  //GPIO Lock
#define GPIOF_APB_AMSEL				*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x528))  //GPIO Analog Mode Select
#define GPIOF_APB_CTL				  *((u32*)(GPIOF_APB_BASE_ADDRESS + 0x52C))  //GPIO Port Control
#define GPIOF_APB_ADCCTL			*((u32*)(GPIOF_APB_BASE_ADDRESS + 0x530))  //GPIO ADC Control





#endif
