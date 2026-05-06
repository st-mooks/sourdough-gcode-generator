encoding = 'utf-8'
gcode_file_path = r'sourdough.gcode'

print("\n***********************************************************\nWelcome to the sourdough heater gcode generator!\nTo use defualt parameters just hit enter for that prompt.\n***********************************************************")

safe_temp_limit = 35 #C
default_temp = 25 #C
default_mode = 'a'
default_days = 7 #days
default_hours = 3 #hours
default_minutes = 30 #minutes
default_cycle_length = 30 #minutes
mode_dict = {'a': 'days',
             'b': 'hours',
             'c': 'minutes'}
try:
    temp = int(input(f"1) What temp to set the heater to? (whole numbers) (default {default_temp}C): ") or default_temp)
    if temp <= 0 or temp > safe_temp_limit:
        print(f'\n***INVALID INPUT. Temp value must be between 0 and {safe_temp_limit}C. Using default temp value ({default_temp}C)***\n')
        temp = default_temp
except:
    print(f"\n***INVALID INPUT. You might have entered a symbol or a letter. Only numbers are allowed. Using default temp value ({default_temp}C)***\n")
    temp = default_temp
mode = input("2) Do you want to heat for:\n   a) days\n   b) hours\n   c) minutes\n(enter a, b, or c) (default days): ") or default_mode
if mode == 'a':
    duration = int(input(f"3) How many days? (whole numbers) (default {default_days} dyas): ") or default_days)
    seconds = duration * 3600 * 24
elif mode == 'b':
    duration = int(input(f"3) How many hours? (whole numbers) (default {default_hours} hours): ") or default_hours)
    seconds = duration * 3600
elif mode == 'c':
    duration = int(input(f"3) How many minutes? (whole numbers) (default {default_minutes} minutes): ") or default_minutes)
    seconds = duration * 60
else:
    mode = 'a'
    print(f"\n***INVALID INPUT. Only acceptable inputs are (a, b, or c). Using default mode ({mode_dict[default_mode]})***\n")
    duration = int(input(f"3) How many days? (whole numbers) (default {default_days} dyas): ") or default_days)
    seconds = duration * 3600 * 24
try:
    cycle_length = int(input("4) To prevent sleep, nudge printer every: (minutes, whole numbers) (default 30 minutes): ") or default_cycle_length)
    if cycle_length <= 0 or cycle_length >= seconds / 60:
        cycle_length = default_cycle_length if default_cycle_length <= seconds / 60 else int(seconds / 60)
        print(f'\n***INVALID INPUT. Nudge value must be larger than 0 and less than the duration specified. Using default nudge value ({default_cycle_length} minutes)***\n')
except:
    print(f"\n***INVALID INPUT. You might have entered a symbol or a letter. Only numbers are allowed. Nudge value set to ({default_cycle_length} minutes)***\n")
    cycle_length = default_cycle_length

cycle_length *= 60 #convert to seconds
cycles_count = seconds // cycle_length
final_cycle = seconds % cycle_length

g_code = [f'M140 S{temp} ;SET BED TEMP\nM190 S{temp} ;WAIT FOR BED TO REACH TEMP\nM84 ;DISABLE STEPPERS\nM300 S440 P200 ;BEEP WHEN THE TEMP IS REACHED\n;WAIT FOR {duration} {mode_dict[mode]}']

for i in range(cycles_count):
    g_code.append(f'G4 S{cycle_length} M105 M114 ;WAIT FOR {cycle_length} SECONDS THEN REPORT TEMP AND POSITION TO KEEP PRINTER AWAKE')
if final_cycle > 0:
    g_code.append(f'G4 S{final_cycle} ;WAIT FOR {final_cycle} SECONDS')
g_code.append("M140 S0 ;SET BED TEMP TO 0 AT THE END\nM300 S440 P200 ;BEEP WHEN FINSHED")
g_code = '\n'.join(g_code)

file_name = f"{duration}_{mode_dict[mode]}_{temp}C_{gcode_file_path}"

with open(file_name, "w", encoding=encoding) as file:
    file.write(g_code)

equal_signs = '=='
dashes = ''
for i in range(len(file_name)):
    equal_signs += '='
    dashes += '-'

input(f"{equal_signs}\ngcode file created successffully as:\n{file_name}\n{dashes}\nTemp: {temp}C.\nDuration: {duration} {mode_dict[mode]}.\nNudge printer every: {int(cycle_length / 60)} minutes.\n{equal_signs}\nPress Enter/Return to exit...\n{equal_signs}")