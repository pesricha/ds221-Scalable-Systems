import pathlib
import subprocess

base_dir = pathlib.Path(__file__).parent.resolve()
input_path = "SameSizeTests"
def run_command(i):
    command = f"{base_dir}/A1/main"
    args = [
        f"{base_dir}/{input_path}/{i}_input_product.csv",
        f"{base_dir}/{input_path}/{i}_input_customer.csv",
        f"{base_dir}/{input_path}/{i}_input_price.csv",
        f"{base_dir}/{input_path}/{i}_input_groups.csv",
        f"{base_dir}/A1/tests_Q1/my_output_Q1.csv",
        f"{base_dir}/A1/tests_Q2/my_output_Q2.csv",
        f"{base_dir}/A1/tests_Q3/My_outputs_Q3",
        f"{base_dir}/{input_path}/{i}_input_newhashtags.csv"
    ]
    
    try:
        result = subprocess.run([command] + args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")
        print("Output:\n", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing command")
        print("Error message:\n", e.stderr.decode())

if __name__ == "__main__":
    
    for i in range(30):
        run_command(i+1)
        print("\n\n")