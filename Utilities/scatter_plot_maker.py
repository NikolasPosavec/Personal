import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

def generate_scatter_plot(x, y, title='Scatter Plot', xlabel='X-axis', ylabel='Y-axis', best_fit=False):
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c='blue', alpha=0.6, edgecolors='black')
    
    # Apply scientific notation to axes
    plt.gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
    
    if best_fit:
        m, b = np.polyfit(x, y, 1)
        # Format coefficients in scientific notation
        m_str = "{:.3e}".format(m)
        b_str = "{:.3e}".format(b)
        plt.plot(x, m*np.array(x) + b, color='red', linestyle='--', 
                label=f'Best Fit Line: y = {m_str}x + {b_str}')
        plt.legend()
        plt.text(min(x), max(y) - (max(y) - min(y)) * 0.1, 
                f'y = {m_str}x + {b_str}', 
                fontsize=12, color='red', verticalalignment='top', 
                bbox=dict(facecolor='white', alpha=0.5))
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.show()

def main():
    choice = input("Enter 'manual' to input data points or 'random' for random points: ").strip().lower()
    
    if choice == 'manual':
        x = list(map(float, input("Enter X values separated by spaces: ").split()))
        y = list(map(float, input("Enter Y values separated by spaces: ").split()))
        if len(x) != len(y):
            print("Error: X and Y must have the same number of values.")
            return
    elif choice == 'random':
        n = int(input("Enter the number of points: "))
        scale = float(input("Enter the maximum value for random numbers (e.g., 1e6): ") or "100")
        x = np.random.rand(n) * scale
        y = np.random.rand(n) * scale
    else:
        print("Invalid choice. Please enter 'manual' or 'random'.")
        return
    
    title = input("Enter title for the graph: ")
    xlabel = input("Enter label for X-axis: ")
    ylabel = input("Enter label for Y-axis: ")
    best_fit = input("Would you like to include a best fit line? (yes/no): ").strip().lower() == 'yes'
    
    generate_scatter_plot(x, y, title=title, xlabel=xlabel, ylabel=ylabel, best_fit=best_fit)

if __name__ == "__main__":
    main()

## paste these lines to run the code (take out comments):

#python3 -m venv venv

#source venv/bin/activate

#pip install matplotlib

#python3 scatter_plot_maker.py