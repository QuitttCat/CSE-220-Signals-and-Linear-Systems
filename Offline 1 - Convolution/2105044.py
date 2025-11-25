import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import os


class DiscreteSignal:
    def __init__(self, INF: int):
        self.INF = INF
        self.values = np.zeros(2 * INF + 1) 
    
    def set_value_at_time(self, time: int, value: float):
        
        if -self.INF <= time <= self.INF:
            self.values[time + self.INF] = value  

    def shift_signal(self, shift: int): 

        shifted_signal = DiscreteSignal(self.INF)
        shifted_signal.values = np.roll(self.values, shift) 

        if shift > 0:
         shifted_signal.values[:shift] = 0
        elif shift < 0:
         shifted_signal.values[shift:] = 0
    
        return shifted_signal

    def add(self, other):

        result_signal = DiscreteSignal(self.INF)
        result_signal.values = self.values + other.values
        return result_signal
    
    def multiply(self, other):
        
        result_signal = DiscreteSignal(self.INF)
        result_signal.values = self.values * other.values
        return result_signal
    
    def multiply_const_factor(self, scaler: float):
       
        result_signal = DiscreteSignal(self.INF)
        result_signal.values = self.values * scaler
        return result_signal
    
    def plot(self, title='Discrete Signal', y_range=(-1,1), figsize=(8,3), x_label='n (Time Index)', y_label='x[n]', saveTo=None):

        plt.figure(figsize=figsize)
        plt.xticks(np.arange(-self.INF, self.INF + 1, 1))
        min_y=np.min(self.values)-1
        max_y=np.max(self.values)+1
        plt.ylim(min_y,max_y)
        plt.stem(np.arange(-self.INF, self.INF + 1, 1), self.values)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        if saveTo is not None:
            plt.savefig(saveTo)
        else:
            plt.show()
       
class ContinuousSignal:
    def __init__(self, func,INF: int):
        self.func = func
        self.INF = INF

    def set_function(self, func):
        self.func = func

    def integrate(self):

        result, _ = quad(self.func, -self.INF, self.INF)
        return result

    def shift_signal(self, shift_value):
        shifted_func = lambda t: self.func(t - shift_value)
        return ContinuousSignal(shifted_func,self.INF)

    def add(self, other):
        combined_func = lambda t: self.func(t) + other.func(t)
        return ContinuousSignal(combined_func,self.INF)

    def multiply(self, other):
        combined_func = lambda t: self.func(t) * other.func(t)
        return ContinuousSignal(combined_func,self.inf)

    def multiply_const_factor(self, scaler: float):
        scaled_func = lambda t: self.func(t) * scaler
        return ContinuousSignal(scaled_func,self.INF)

    def plot(self, num_points=1000, title='ContinuousSignal', y_range=None, figsize=(8, 6), x_label='t', y_label='x(t)', saveTo=None):
        t_values = np.linspace(-self.INF,self.INF, num_points)
        y_values = self.func(t_values)
        plt.figure(figsize=figsize)
        plt.plot(t_values, y_values, label='x(t)')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        if y_range:
            plt.ylim(y_range)
        
        plt.grid(True)
        plt.legend()

        if saveTo:
            plt.savefig(saveTo)
        else:
            plt.show()

class LTI_Discrete:
    def __init__(self, impulse_response: DiscreteSignal):

        self.impulse_response = impulse_response

    def linear_combination_of_impulses(self, input_signal: DiscreteSignal):
    
        impulses = []
        coefficients = []
        

        for i in range(-input_signal.INF, input_signal.INF + 1):
            coeff = input_signal.values[i + input_signal.INF]
            impulse = DiscreteSignal(input_signal.INF)
            impulse.set_value_at_time(i, 1)  
            impulses.append(impulse)
            coefficients.append(coeff)

         

        return impulses, coefficients

    def output(self, input_signal: DiscreteSignal):
        
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        output_signal = DiscreteSignal(input_signal.INF)

        for impulse, coeff in zip(impulses, coefficients):
           
            time_index = np.where(impulse.values == 1)[0][0] - input_signal.INF
            response_to_impulse = self.impulse_response.shift_signal(time_index)
            output_signal = output_signal.add(response_to_impulse.multiply_const_factor(coeff))
        
        return output_signal
    
    
    def show_decomposition_input(self, input_signal: DiscreteSignal,saveTo=None):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        
       
        num_plots = len(impulses) + 1 
        num_cols = 3
        num_rows = (num_plots + num_cols - 1) // num_cols 
        
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12,8))
        fig.suptitle('Impulses multiplied by coefficients')

        plt.subplots_adjust(hspace=1.5, wspace=1)
        axs = axs.flatten()  


        for idx, (impulse, coeff) in enumerate(zip(impulses, coefficients)):
            time_index = np.where(impulse.values == 1)[0][0] - input_signal.INF
            response_to_impulse = impulse
            contribution = response_to_impulse.multiply_const_factor(coeff)
        

            axs[idx].stem(np.arange(-input_signal.INF, input_signal.INF + 1, 1), contribution.values)
            axs[idx].set_title(f"$\\delta[n-({time_index})] x[{time_index}]$")

            axs[idx].set_xlabel('n (Time Index)')
            axs[idx].set_ylabel('x[n]')
            axs[idx].grid(True)

            axs[idx].set_ylim(np.min(input_signal.values) - 1, np.max(input_signal.values) + 1)
            axs[idx].set_xticks(np.arange(-input_signal.INF, input_signal.INF + 1))
            axs[idx].set_yticks(np.arange(np.min(input_signal.values)-1, np.max(input_signal.values) + 1))
           

        axs[len(impulses)].stem(np.arange(-input_signal.INF, input_signal.INF + 1, 1), input_signal.values)
        axs[len(impulses)].set_ylim(min(input_signal.values)-1, max(input_signal.values) + 1)
        axs[len(impulses)].set_title("Sum")
        axs[len(impulses)].set_xlabel('n (Time Index)')
        axs[len(impulses)].set_ylabel('x[n]')
        axs[len(impulses)].grid(True)
        axs[len(impulses)].set_xticks(np.arange(-input_signal.INF, input_signal.INF + 1))
        axs[len(impulses)].set_yticks(np.arange(np.min(input_signal.values), np.max(input_signal.values) + 1))
    
        for i in range(num_plots, len(axs)):
            fig.delaxes(axs[i])

        plt.tight_layout()
        plt.grid(True)
        

        if saveTo:
            plt.savefig(saveTo)
        else:
            plt.show()
    
    def show_decomposition_output(self, input_signal: DiscreteSignal,saveTo=None):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        
       
        num_plots = len(impulses) + 1 
        num_cols = 3
        num_rows = (num_plots + num_cols - 1) // num_cols 
        
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12,8))
        fig.suptitle('Impulses multiplied by coefficients')

        plt.subplots_adjust(hspace=1.5, wspace=1)
        axs = axs.flatten()  
        output_signal = self.output(input_signal)

        for idx, (impulse, coeff) in enumerate(zip(impulses, coefficients)):
            time_index = np.where(impulse.values == 1)[0][0] - input_signal.INF
            response_to_impulse = self.impulse_response.shift_signal(time_index)
            contribution = response_to_impulse.multiply_const_factor(coeff)
        

            axs[idx].stem(np.arange(-input_signal.INF, input_signal.INF + 1, 1), contribution.values)
            axs[idx].set_title(f"$h[n-({time_index})] x[{time_index}]$")

            axs[idx].set_xlabel('n (Time Index)')
            axs[idx].set_ylabel('x[n]')
            axs[idx].grid(True)

            axs[idx].set_ylim(np.min(output_signal.values) - 1, np.max(output_signal.values) + 1)
            axs[idx].set_xticks(np.arange(-input_signal.INF, input_signal.INF + 1))
            axs[idx].set_yticks(np.arange(np.min(output_signal.values)-1, np.max(output_signal.values) + 1))
           

        axs[len(impulses)].stem(np.arange(-input_signal.INF, input_signal.INF + 1, 1), output_signal.values)
        axs[len(impulses)].set_ylim(min(output_signal.values)-1, max(output_signal.values) + 1)
        axs[len(impulses)].set_title("Output = Sum")
        axs[len(impulses)].set_xlabel('n (Time Index)')
        axs[len(impulses)].set_ylabel('x[n]')
        axs[len(impulses)].grid(True)
        axs[len(impulses)].set_xticks(np.arange(-input_signal.INF, input_signal.INF + 1))
        axs[len(impulses)].set_yticks(np.arange(np.min(output_signal.values), np.max(output_signal.values) + 1))
    
        for i in range(num_plots, len(axs)):
            fig.delaxes(axs[i])

        plt.tight_layout()
        plt.grid(True)
        

        if saveTo:
            plt.savefig(saveTo)
        else:
            plt.show()
class LTIContinuous:
    def __init__(self, impulse_response: ContinuousSignal):
        self.impulse_response = impulse_response
    
    def linear_combination_of_impulses(self, input_signal: ContinuousSignal, delta: float):
        impulses = []
        coefficients = []
        
   
        t_values = np.arange(-input_signal.INF, input_signal.INF, delta)
        
        for t in t_values:
            

            if abs(t) < 1e-9:
                 coeff = delta 
            else:
                 coeff = input_signal.func(t)*delta  
           
            # print(coeff)
            coefficients.append(coeff)
            contsig=ContinuousSignal(lambda tau,t=t,delta=delta: (1/delta)*((t<=tau) & (tau<t+delta)), input_signal.INF)
            # contsig.plot()
            impulses.append(contsig)
        
        # for i in range(len(impulses)):
        #     impulses[i].plot()
        
        return impulses, coefficients
    
    def output_approx(self, input_signal: ContinuousSignal, delta: float):
        
        # impulses, coefficients = self.linear_combination_of_impulses(input_signal, delta)
        
        
        responses= []
        
        time_range = np.arange(-input_signal.INF, input_signal.INF,delta)
       
        for i in time_range:
            
            # shifted_impulse_response = self.impulse_response.shift(i)
            # shifted_impulse_response = shifted_impulse_response.multiply_const_factor(coefficent)            
            if abs(i) < 1e-9:
                coefficent = delta
            else:
                coefficent = input_signal.func(i)*delta 
            shifted_impulse_response = self.impulse_response.shift_signal(i)
            shifted_impulse_response = shifted_impulse_response.multiply_const_factor(coefficent)
            contsig=ContinuousSignal(shifted_impulse_response.func, input_signal.INF)

            responses.append(contsig)
            

           
        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
        reconstructed_values = np.zeros(1000)    

        for i in range(len(responses)):
         
         impulse_values = responses[i].func(t_values)
         reconstructed_values += impulse_values

        final_output = reconstructed_values


        return responses,final_output



        
    

    def reconstrct_input(self, input_signal: ContinuousSignal, delta: float, saveTo=None):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal, delta)
        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
        reconstructed_values = np.zeros(1000)

        for i in range(len(impulses)):
         
         impulse_values = impulses[i].func(t_values)*coefficients[i]
         reconstructed_values += impulse_values

        return reconstructed_values
    
    def actual_reconstructed_input_plot(self, input_signal: ContinuousSignal,deltaarry,saveTo=None):
        
        num_cols = 2
        num_plots = len(deltaarry) 
        num_rows = (num_plots + num_cols - 1) // num_cols

        fig, axs = plt.subplots(num_rows,num_cols, figsize=(10, 8))
        fig.suptitle('Actual vs Reconstructed  Input Signal for Different Δ', fontsize=15)
        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
        actual_values=input_signal.func(t_values)

        plt.subplots_adjust(hspace=0.5, wspace=0.4)
        axs = axs.flatten()  

        for i in range(len(deltaarry)):
         reconstructed_values = self.reconstrct_input(input_signal,deltaarry[i])
         axs[i].plot(t_values, reconstructed_values, label='Reconstructed')
         axs[i].plot(t_values,actual_values, label='x(t)', color='orange')
         axs[i].set_title(f'$\\nabla = {deltaarry[i]}$')
         axs[i].set_xlabel('t (Time)')
         axs[i].set_ylabel('x(t)')
         axs[i].legend()
         axs[i].grid(True)


        plt.tight_layout()

        if saveTo:
         plt.savefig(saveTo)
        else:
         plt.show()


    def actual_reconstructed_output_plot(self, input_signal: ContinuousSignal,deltaarry,saveTo=None):
        
        num_cols = 2
        num_plots = len(deltaarry) 
        num_rows = (num_plots + num_cols - 1) // num_cols

        fig, axs = plt.subplots(num_rows,num_cols, figsize=(10, 8))
        fig.suptitle('Approximate Output Δ tends to 0', fontsize=15)
        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
        actual_values=input_signal.func(t_values)
        time_range = np.linspace(-input_signal.INF, input_signal.INF , 1000)
        integrated_value=(1 - np.exp(-time_range)) * (time_range >= 0)

        plt.subplots_adjust(hspace=0.5, wspace=0.4)
        axs = axs.flatten()  

        for i in range(len(deltaarry)):
         responses,reconstructed_values = self.output_approx(input_signal,deltaarry[i])
         axs[i].plot(t_values, reconstructed_values, label='y_approx(t)')
         axs[i].plot(t_values,integrated_value, label='y(t)=(1-e^(-t)u(t))', color='orange')
         axs[i].set_title(f'$\\nabla = {deltaarry[i]}$')
         axs[i].set_xlabel('t (Time)')
         axs[i].set_ylabel('x(t)')
         axs[i].legend()
         axs[i].grid(True)


        plt.tight_layout()

        if saveTo:
         plt.savefig(saveTo)
        else:
         plt.show()

    
    def show_decomposition_input(self, input_signal: ContinuousSignal, delta: float, saveTo=None):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal, delta)

        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
        reconstructed_values = np.zeros(1000)

        for i in range(len(impulses)):
         
         impulse_values = impulses[i].func(t_values)*coefficients[i]
         reconstructed_values += impulse_values

        y_min = reconstructed_values.min()
        y_max = reconstructed_values.max()

        num_plots = len(impulses) + 2
        num_cols = 3
        num_rows = (num_plots + num_cols - 1) // num_cols

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 12))
        fig.suptitle('Impulses multiplied by coefficient')
        plt.subplots_adjust(hspace=1.5, wspace=1)
        axs = axs.flatten()

        numbering=-(1/delta)*input_signal.INF

        for i in range(len(impulses)):
         impulse_values = impulses[i].func(t_values)*coefficients[i]
    
         axs[i].plot(t_values, impulse_values)
         axs[i].set_title(f'$\\delta(t - ({numbering}\\nabla)) x({numbering}\\nabla) \\nabla$')
         axs[i].set_ylim(y_min-.2 , y_max+.2)
         axs[i].set_xlabel('t(Time)')
         axs[i].set_ylabel('x[n]')
       
         axs[i].grid(True)
         numbering+=1


        axs[len(impulses) ].plot(t_values,reconstructed_values,label="Reconstructed Signal")
        axs[len(impulses) ].set_title("Reconstructed Signal")
        axs[len(impulses)].set_ylim(y_min-.2, y_max+.2)
        axs[len(impulses)].set_xlabel('t(Time)')
        axs[len(impulses)].set_ylabel('x[n]')
        axs[len(impulses) ].grid(True)

        for i in range(num_plots, len(axs)):
         fig.delaxes(axs[i])

        plt.tight_layout()

        if saveTo:
         plt.savefig(saveTo)
        else:
         plt.show()



    def show_decomposition_output(self, input_signal: ContinuousSignal, delta: float, saveTo=None):

        responses,final_output = self.output_approx(input_signal,delta)

        t_values = np.linspace(-input_signal.INF, input_signal.INF, 1000)
    
        # for i in range(len(impulses)):
        #  coefficent = input_signal.func(i)
        #  shifted_impulse_response = self.impulse_response.shift(i)
        #  shifted_impulse_response = shifted_impulse_response.multiply_const_factor(coefficent) 
        #  reconstructed_values += impulse_values

        y_min = np.min(final_output)
        y_max = np.max(final_output)


        num_plots = len(responses) + 1
        num_cols = 3
        num_rows = (num_plots + num_cols - 1) // num_cols

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 12))
        fig.suptitle('Response of impulse signal')
        plt.subplots_adjust(hspace=1.5, wspace=1)
        axs = axs.flatten()

        numbering=-(1/delta)*input_signal.INF

        for i in range(len(responses)):
         
         output_values=responses[i].func(t_values)
         axs[i].plot(t_values,output_values)
         axs[i].set_title(f'$h(t - ({numbering}\\nabla)) x({numbering}\\nabla) \\nabla$')
         axs[i].set_ylim(y_min-.2 , y_max+.2)
         axs[i].set_xlabel('t(Time)')
         axs[i].set_ylabel('x[n]')
         axs[i].grid(True)
         numbering+=1


        axs[len(responses)].plot(t_values,final_output,label="Output = sum")
        axs[len(responses)].set_title("Reconstructed Signal")
        axs[len(responses)].set_ylim(y_min-.2, y_max+.2)
        axs[len(responses)].set_xlabel('t(Time)')
        axs[len(responses)].set_ylabel('x[n]')
        axs[len(responses) ].grid(True)

        for i in range(num_plots, len(axs)):
         fig.delaxes(axs[i])

        plt.tight_layout()

        if saveTo:
         plt.savefig(saveTo)
        else:
         plt.show()

    
           





    


    
def main():
    # Create directories for saving files if they don't exist
    os.makedirs('discrete', exist_ok=True)
    os.makedirs('continuous', exist_ok=True)

    # Discrete signals
    input_signal = DiscreteSignal(INF=5)
    input_signal.set_value_at_time(0, 0.5)
    input_signal.set_value_at_time(1, 2)
    input_signal.plot(saveTo='discrete/Input_Discrete_Signal.png')

    impulse_response = DiscreteSignal(INF=5)
    impulse_response.set_value_at_time(0, 1)
    impulse_response.set_value_at_time(1, 1)
    impulse_response.set_value_at_time(2, 1)
    impulse_response.plot(saveTo='discrete/Impulse_Response_Discrete.png')

    lti_system = LTI_Discrete(impulse_response)
    # Uncomment to get output of LTI System
    # output_signal = lti_system.output(input_signal)
    # output_signal.plot(title="Output of LTI System", saveTo='discrete/Output_Discrete_LTI.png')

    lti_system.show_decomposition_input(input_signal, saveTo='discrete/Impulses_multiplied_by_coefficient_Discrete.png')
    lti_system.show_decomposition_output(input_signal, saveTo='discrete/Response_of_the_input_signal_Discrete.png')

    # Continuous signals
    def x_t(t):
        return np.where(t < 0, 0, np.exp(-t))

    def impulse_response(t):
        return 1 * (t >= 0)

    input_signal = ContinuousSignal(x_t, 3)
    input_signal.plot(saveTo='continuous/Input_Continuous_Signal.png')

    lambda_value = 0.5
    __impulse_response = ContinuousSignal(impulse_response, 3)
    __impulse_response.plot(saveTo='continuous/Impulse_Response_Continuous.png')

    Clti = LTIContinuous(__impulse_response)
    Clti.show_decomposition_input(input_signal, lambda_value, saveTo='continuous/Impulses_multiplied_by_coefficient_continuous.png')
    deltaarray = [0.5, 0.1, 0.05, 0.01]
    Clti.actual_reconstructed_input_plot(input_signal, deltaarray, saveTo='continuous/Actual_vs_Reconstructed_Input.png')
    Clti.show_decomposition_output(input_signal, lambda_value, saveTo='continuous/Response_of_the_input_signal_continuous.png')
    Clti.actual_reconstructed_output_plot(input_signal, deltaarray, saveTo='continuous/Actual_vs_Reconstructed_Output.png')

# Run the main function
main()
