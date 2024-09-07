def average_duration_per_file(total_hours, total_minutes, num_files):
    # Convert total hours to minutes and add the total minutes
    total_minutes_all = total_hours * 60 + total_minutes
    
    # Convert the total minutes to seconds
    total_seconds = total_minutes_all * 60
    
    # Calculate the average duration in seconds
    average_duration_seconds = round(total_seconds / num_files, ndigits=2)
    
    return average_duration_seconds

# Example usage:
num_files = 27040
total_hours = 81
total_minutes = 2

avg_seconds = average_duration_per_file(total_hours, total_minutes, num_files)
print(f"Average duration per file: {avg_seconds} seconds")
