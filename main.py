import csv
import sys


def time_to_seconds_milliseconds(value):
    # Check if the value contains ':', which indicates it's in MM:SS:MS format
    if ':' in value:
        parts = value.split(':')
        minutes = int(parts[0])
        seconds = int(parts[1].split('.')[0])
        milliseconds = int(parts[1].split('.')[1])

        total_seconds = minutes * 60 + seconds
        return f"{total_seconds}.{str(milliseconds).zfill(2)}"
    else:
        return value


def format_data(input_data):
    output = []
    for row in input_data:
        new_row = [time_to_seconds_milliseconds(val) if ':' in val or '.' in val else val for val in row]
        output.append(new_row)

    return output


def convert_to_cumulative(input_data):
    # Calculate the cumulative sum for each row
    for i in range(1, len(input_data)):
        for j in range(2, len(input_data[i])):
            if input_data[i][j]:
                input_data[i][j] = float(input_data[i][j - 1]) + float(input_data[i][j])
            else:
                input_data[i][j] = ''
    return input_data


if __name__ == "__main__":
    # Read the CSV data
    input_filename = sys.argv[1]
    with open(input_filename, 'r') as infile:
        reader = csv.reader(infile)
        data = [row for row in reader]
    data[0][0] = "Name"

    # Transpose the data
    transposed_data = list(zip(*data))
    formatted_data = format_data(transposed_data)
    cumulative_data = convert_to_cumulative(formatted_data)
    # cumulative_data[0][0] = "Name"

    # Write the transposed data to a new CSV file
    with open('transposed_output.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cumulative_data)

