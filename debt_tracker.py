import pandas as pd  



def strt(num):
    return '%.2f' % num



class deuda:
    """
      Amortizacion FRANCESA : se caracteriza por el pago de casa cuota es siempre constante (siempre la misma)
    """

    def __init__ (self, capital, n_cuotas, interes_anual, seguro_desgravamen=0.0, otros=0.0, nombre='N/A' ):
        
        """
        interes_anual      = (Porcentaje) E.g. 25%
        seguro_desgravamen = (por cuota) E.g. $1.50
        otros              = (por cuota E.g.) E.g  $5.0

        """
        self.nombre =nombre
        self.capital = capital
        self.n_cuotas = n_cuotas
        self.interes_anual = interes_anual /100.0 # Ejemplo si el interes es del 25.5% -> 0.255 : Tasa interés nominal anual 
        self.seguro_desgravamen = seguro_desgravamen
        self.otros = otros
        

        # Variables a conseguir 
        self.total_impuestos =0.0
        self.total_a_pagar =0.0 # monto que me prestaron + los intereses and toda la M que se lleva el bancon u otras entidades
        self.cuota_const = 0.0 #Amoritizacion frances se caracteriza por tener una cuota constante. Usualmente casa mes.
        self.perdida = 0.0#


        self.calcular_valores()


    def calcular_valores(self):

        """
         Crear pandas data frame con las columnas :   Numero de cuota,  a_pagar,  al_capital,  al_interes, capital_pendiente
         
        """
        self.interes_anual /= 12.0
     
        # Calculo de cuota contante
        self.cuota_const = self.capital * self.interes_anual /   ( 1.0 - (  (1.0+self.interes_anual) ** (- self.n_cuotas)  )     )      # << Formula 1 >> 

        print(' La cuota constance mensual es : ' +str(self.cuota_const ) )

        # Calculo de total a pagar : 
        self.total_a_pagar = (self.cuota_const * self.n_cuotas ) + (self.seguro_desgravamen *self.n_cuotas) + ( self.otros * self.n_cuotas)
 
        # Calculo de Perdida
        self.perdida =  ( self.total_a_pagar - self.capital ) # El monto que le estoy dando al banco


       ###################
       # Populating table 
       ####################
       
       #  [ Numero de cuota,  a_pagar,  al_interes,  al_capital, capital_pendiente ]

        data= [[0, 0.0, 0.0, 0.0, self.capital ]] # Initial year : does not really count

        for n in range(1, self.n_cuotas+1 ) :
            
            #Numero de cuota
            # n += 1 # Contamos desde 1 hasta n_cuotas in range inclusivode  [1, n_cuotas] 
            


            #Calculo de lo que va al interes y de lo que va al capital 
            al_interes =  data[n-1][4] * (self.interes_anual) # [ Capital_pendiente PREVIO * interes_anual ]  << Formula 2 >>
            al_capital = self.cuota_const -  al_interes 

            #Calculo de amortizacion del capital - al_capital
            # Esta columna no es infomracion repetida pero la mantenemos  por consistencia.
            a_pagar = self.cuota_const +   self.seguro_desgravamen  +  self.otros
        
            #Calculo de lo que me hace falta pagar
            capital_restante =  data[n-1][4] - al_capital 
            capital_restante = 0.0 if  capital_restante < 0  else  capital_restante

            data.append( [n  , a_pagar , al_interes, al_capital,  capital_restante ] )


        # Transform to df
        self.df = pd.DataFrame.from_records(data, columns=[ 'Numero de Cuota',  'Cuota Mensual' ,  'Al interes' ,  'Al capital' , 'Capital pendiente' ] )
    

    def print_debt(self,  cuota_ref=0 ):

        """
        couta_ref = es el numero de cuota utilizado para  calcular de aquel numero de couta en adelante
        """

        perdida= self.df.iloc[cuota_ref: self.n_cuotas,2]# Solo toma en cuenta interesee, desgravamenes + otros no son considerados
        perdida = perdida.sum()


        print ( '\n\n---------------------------------------------------------------------')
        print(  '                       Deuda : ' +str(self.nombre) )
        print ( '---------------------------------------------------------------------')
        print(' Perdida TOTAL(incluye seguro + otros)' + strt(self.perdida))

        print('\nPerdida en intereses(Lo que se puede ahorrar )        : $ ' + strt(perdida) ) 
        print('Para Acabar la deuda hoy dia (Pago Total) : $ ' +strt(self.df.iloc[cuota_ref,4]) )
        print('Caso contrario, para acabar la deuda  en '+ str(self.n_cuotas-cuota_ref) +' meses ('+strt( (self.n_cuotas-cuota_ref)/12.0 )+' años):  $ '+strt(self.cuota_const*(self.n_cuotas-cuota_ref) )     )
        print ('\n\n')







#####################
##  Deuda Presente 
######################




class deuda_presente ():

    def __init__ (self, cuota_mensual,  capital_previo , n_cuotas, cuota_presente, interes_anual,   seguro_mensual = 0.0, otros_mensual=0.0, nombre=None):
        
        
        self.cuota_mensual = cuota_mensual # la que es calculada con la formula. Sin agregar seguro, ni
        self.capital_previo = capital_previo # capital del mes pasado
        self.n_cuotas = n_cuotas
        self.cuota_presente = cuota_presente
        self.interes_anual = interes_anual/100.0 # E.g. Pass it as 25.5 for (25.5%)
        self.seguro_mensual = seguro_mensual
        self.otros_mensual =otros_mensual
        self.nombre= nombre
       
        self.main_df= self.calcular()

    def calcular (self, monto_a_capital=0.0, monto_mensual=0.0 ):

        #Initial acorde a la cuota presente


         # Need to calculate the table all over again 

        a_pagar =self.cuota_mensual+ self.seguro_mensual+ self.otros_mensual

        # numero de couta,  Pago Mensual,  Al interes ,  Al Capital , Capital Pendiente ]
        interes_mensual = self.interes_anual /12.0
        al_interes = self.capital_previo*interes_mensual
        al_capital = self.cuota_mensual -  al_interes 

        if monto_a_capital > 0.0 :
            capital_pendiente = self.capital_previo -  al_capital - monto_a_capital
        elif monto_mensual > 0.0 :
            capital_pendiente = self.capital_previo -  al_capital - monto_mensual
        else:
            capital_pendiente = self.capital_previo -  al_capital 

        cuenta_presente = self.cuota_presente

        data= [[cuenta_presente, a_pagar,  al_interes  , al_capital , capital_pendiente]] 

        data_pointer = 0


        while( round( capital_pendiente , 2 )> 0.0 ) :
            data_pointer+=1

            #Calculo de lo que va al interes y de lo que va al capital 
            al_interes =  data[data_pointer-1][4] * (interes_mensual) # [ Capital_pendiente PREVIO * interes_anual ]  << Formula 2 >>
            
            if  monto_mensual > 0.0 :
                al_capital = self.cuota_mensual -  al_interes  + monto_mensual
            else:
                 al_capital = self.cuota_mensual -  al_interes
            #Calculo de amortizacion del capital - al_capital
            # Esta columna no es infomracion repetida pero la mantenemos  por consistencia.
            a_pagar = self.cuota_mensual +   self.seguro_mensual  +  self.otros_mensual
            #Calculo de lo que me hace falta pagar
            capital_pendiente =  data[data_pointer-1][4] - al_capital 
            cuenta_presente +=1
            

            data.append( [cuenta_presente, a_pagar , al_interes, al_capital,  capital_pendiente ] )
        

         # Transform to df
        return pd.DataFrame.from_records(data, columns=[ 'Numero de Cuota',  'Cuota Mensual' ,  'Al interes' ,  'Al capital' , 'Capital pendiente' ] )


    

    def print_total_debt(self):
        self.print_deuda_presente(self.main_df)


    def print_deuda_presente(self , dff , silent=False):

        """

        couta_ref = es el numero de cuota utilizado para  calcular de aquel numero de couta en adelante
        """
      

        perdida_total = dff['Cuota Mensual'].sum()# Solo toma en cuenta interesee, desgravamenes + otros no son considerados

        capital_present = dff.iloc[0 , 4]

        if not silent:
            print ( '\n\n---------------------------------------------------------------------')
            print(  '                       Deuda : ' +str(self.nombre) )
            print ( '---------------------------------------------------------------------')

            print (" Total a pagar hasta final de deuda ( incluye seguro y otros) $ " + strt(perdida_total))
            print( " Lo que realmente se debe (Capital presente) : $ "+strt(capital_present))        
            print( " Ahorro Potencial (Lo que se queda el banco) : $ "+strt(perdida_total-capital_present ) + ' <------------' )

            print ('\n\n')

        return dff['Al interes'].sum()

    
    def si_pago(self, monto_mensual=0.0, monto_a_capital=0.0):
        """
         Only one at the time can be applied 
        """


        original_interes = self.print_deuda_presente(self.main_df, silent=True)
        si_df = self.calcular(monto_mensual=monto_mensual, monto_a_capital=monto_a_capital)        
        si_interes= self.print_deuda_presente(si_df, silent=True)

        # print (" \n\n SI pago :     ")
        print(si_df)

     

        print('\n\n')

        if monto_mensual > 0.0 :
            print (" Pagando un monto mensual de $ "+strt(monto_mensual) +' cada mes ahorramos (SOLO INTERESES) : $ '+strt(original_interes-si_interes) )

        if monto_a_capital > 0.0 :
            print (" Pagando un monto unico HOY DIA de $ "+strt(monto_a_capital) +'  ahorramos (SOLO INTERESES): $ '+strt(original_interes-si_interes) )

        return original_interes-si_interes

        







       
        









##############
# MAIN
##############

#     """
#     This is a way to model the family debt based on the  amortizacion Francesa
#     """

pd.options.display.float_format = "{:.2f}".format


# pichincha = deuda_presente(467.15, 10000 , 24, 1, 11.23,   seguro_mensual = 0.0, otros_mensual= 0.0, nombre='Pichincha' )
# pichincha.print_total_debt()
# pichincha.si_pago(monto_a_capital=1500.0)
# pichincha.si_pago( monto_mensual=1500.0)

# (self, cuota_mensual,  capital_previo , n_cuotas, cuota_presente, interes_anual,   seguro_mensual = 0.0, otros_mensual=0.0, nombre=None):
cooprogreso= deuda_presente(1043.02, 67261.82 , 126, 22, 10.48,   seguro_mensual = 0.0, otros_mensual= 0.0, nombre='Cooprogreso' )
cooprogreso.print_total_debt()


# cooprogreso.si_pago( monto_mensual=100.0)
cooprogreso_ahorro = cooprogreso.si_pago(monto_a_capital=2000.0)


coopad =deuda_presente(547.5, 8312.32, 34,16,15.5, nombre='Coopad' )

coopad_ahorro =coopad.si_pago(monto_a_capital=2000.0)


print("\n\n")
print ('Ahorro en Cooprogreso : $' +strt(cooprogreso_ahorro) )
print('Ahorra en Coopad : $' +strt(coopad_ahorro))




print('  \n\n-------    End of the Program     -------    ')
