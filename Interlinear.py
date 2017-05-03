from tkinter import messagebox
import tokenize
import os
import codecs


class Interlinear(object):
    def __init__(self):
        self.filename = ""

def create(txt1, txt2):
    #message_start_instructions()
    txt1 = txt1.replace('\n', '')
    txt1 = txt1.replace('\r\n', '')
    txt2 = txt2.replace('\n', '')
    txt2 = txt2.replace('\r\n', '')

    # If user cancels, exit.
    if len(txt1) < 1 or len(txt2) < 1:
        exit()
    # Get file names
    file1_name = os.path.basename(txt1)
    file2_name = os.path.basename(txt2)

    # Check to see if the the file has trailing numbers.
    f1_numbered = check_file_name_for_number(file1_name)  # Returns True or False
    f2_numbered = check_file_name_for_number(file2_name)  # Returns True or False

    if f1_numbered and f2_numbered:
        repeat = True  # Enable for sequential file operation.
    else:
        repeat = False  # Not sequential, do only one file.
    # If trailing numbers are present, get string form of file number, else just use plain file name
    file_out = ''
    if repeat:
        # First check to make sure the file numbers match
        str_f1_number = get_number_from_file(file1_name)
        str_f2_number = get_number_from_file(file2_name)
        if str_f1_number == str_f2_number:
            file_out = "Interlinear-Vol" + str_f1_number + ".srt"  # Sequential operation
        else:
            message_mismatched_file_numbers(file1_name, file2_name)  # Mismatch in file numbers.
            exit()  # Test failed, exit
    else:
        file_out = "Interlinear.srt"  # One file  only

    # File name and path have been resolved, begin processing
    #loop = 0  # For debugging
    go = True
    while go:
        er1 =check_for_UTF_8(txt1)  # Check file1 for UTF-8 encoding.
        if not er1:
            message_not_UTF_8(txt1)
            return 0
        er2 = check_for_UTF_8(txt2)  # Check file2 for UTF-8 encoding.
        if not er2:
            message_not_UTF_8(txt2)
            return 0
        f1 = open_file(txt1)  # Passed UTF-8 test, open file
        f2 = open_file(txt2)  # Passed UTF-8 test, open file
        txt_for_f3 = ''
        # Files are good, go
        for line in f1:
            while line == '\r\n':  # Check for blank lines at the beginning.
                line = f1.readline()  # Remove line but don't use
                f2.readline()  # Remove line but don't use
            '''line_test = line.replace('\r\n', '')  # FOR DEBUGGING
            line_number_to_stop_at = '257'        # FOR DEBUGGING
            if line_number_to_stop_at == line_test and loop == 1:  # FOR DEBUGGING
                print(line_test)                                    # FOR DEBUGGING
            '''
            # GET section from f1, [number, timing line, and text].  If there are two lines of text, merge them.
            txt_for_f3 = get_section_from_f1(txt_for_f3, f1, line)

            # Remove section number and timing line from f2, but do not use, extract text only
            text_line1 = f2.readline().lstrip()
            section_number = replace_eleven_and_thirty(text_line1)  # Line only used to check for mismatch.
            f2.readline().lstrip()  # Remove line but don't use
            if line != section_number:  # Check for section number mismatch
                message_display_alert_if_line_mismatch(line, section_number, txt1, txt2)
                return 0

            # Get text from second language subtitles, this is the only thing taken from the section.
            txt_for_f3 = get_section_from_f2(txt_for_f3, f2)  # EXTRACT TEXT ONLY

        file_path3 = os.path.dirname(txt1) + '/' + file_out
        f3 = codecs.open(file_path3, encoding='utf-8', mode='w')
        f3.write(txt_for_f3)
        f1.close()
        f2.close()
        f3.close()
        if not repeat:
            message_bad_file_name()
            return 0

        if file1_name[-6:-4].isnumeric():
            file1_name = inc_filename(file1_name)
        else:
            message_bad_file_name()
            return 0

        if file2_name[-6:-4].isnumeric():
            file2_name = inc_filename(file2_name)
        else:
            message_bad_file_name()
            return 0

        # If looping to next two files, increment the number in the file string
        txt1 = os.path.dirname(txt1) + "/" + file1_name
        txt2 = os.path.dirname(txt2) + "/" + file2_name
        file_out = inc_filename(file_out)
        if not os.path.exists(txt1):
            message_file_does_not_exist(txt1)
            return 0
        else:
            if not os.path.exists(txt2):
                message_file_does_not_exist(txt2)
                return 0
            else:
                continue

# Get on set of (line number, timing line, and the two text lines).
def get_section_from_f1(txt, f, line):
    # Add the section number in line to the header
    # Peel off one more line from f, the time line.
    header = line + rm_err_chars(f.readline())
    # Get text from first language subtitle file
    txt += header
    line = f.readline().lstrip()
    while line != "\r\n" and len(line) > 0:
        txt = txt + line.replace('\r\n', " ")  # + CRLF  #  Case = Text in second line
        line = f.readline()
    # Last line peeled off in the while will be the blank space.
    txt += "\r\n"
    return txt

# Starts with text lines, not the number or the timing line
def get_section_from_f2(txt, f2):
    line = f2.readline().lstrip()
    while line != "\r\n" and len(line) > 0:
        txt = txt + line.replace('\r\n', " ")  # Case = Text in second line
        line = f2.readline().lstrip()
    return txt + "\r\n\r\n"


# Returns number part of the file as a string, but does not inc it as above
def get_number_from_file(filename):
    filename = filename.replace('.srt', '')
    filename = filename.replace('.txt', '')
    num_str = filename[-2:]
    if num_str.isnumeric():
        num1 = int(num_str)
        if num1 < 10:
            return '0' + str(num1)
        else:
            return str(num1)
    else:
        message_bad_file_name()
        return 0


def message_start_instructions():
    messagebox.showinfo(title="Interlinear Subtitle Creator Version 1.0 - Coded by Shawn Irwin",
            message='''Get Files - Both files you select should be saved in UTF-8 format!
            (Notepad can do this.) The first file you select will be the
            language displayed on the top line of the subtitle. The second
            file you select will be the language displayed on the bottom line
            of the subtitle.  The interlinear file created will be saved in
            the same directory as the first file you select.''')

def message_mismatched_lines():
    messagebox.showerror(title="Mismatched lines", message='Mismatched lines between file1 and file2.')

def message_mismatched_file_numbers(f1, f2):
    msg  = 'Mismatched file numbers between ' + f1 + ' and ' + f2
    messagebox.showerror(title="Mismatched file numbers", message=msg)

def message_bad_file_name():
    messagebox.showerror(title="File name.", message='''If you needed to process only one file, it has been  completed,
click OK, and ignore this message.

If you want to process a sequence of files, the file names of each set
must have TWO digits at the END of the file names, numbered
sequentially.  For example . . .

  Language subtitle file set one:
       L1file01.srt, L1file02.srt, etc. .

  Language subtitle file set two:
       L2file01.srt, L2file02.srt, etc.''')

def message_file_does_not_exist(pth):
    messagebox.showerror(title="Non-existing file", message='Error - ' + pth +' does not exist . . . ')

def message_not_UTF_8(filename):
    message_utf = 'File not saved in UTF-8 format.'
    messagebox.showerror(title=message_utf, message='Error - ' + filename + ' not saved in UTF-8 format. \r\n'
                    '\r\nSave it in UTF-8 encoding format.\r\n\r\nIf there are spaces at the beginning of the subtitle\r\n' +
                    'lines you could also get this error. \r\n\t\n                 Exiting . . . ')

def message_display_alert_if_line_mismatch(ln, hd_2, f1path, f2path):
        messagebox.showinfo(title="Merge Subtitle Files",
                            message="Mismatched lines: First - - - \r\n" + ln + "Second - " + hd_2
                                    + "\r\n" + f1path + "\r\n" + '\r' + f2path + "\r\n")


def message_display_alert_unknown_error(ln, hd_2, f1path, f2path):
    messagebox.showinfo(title="Merge Subtitle Files",
                        message="unknown error near lines: First - - - \r\n" + ln + "Second - " + hd_2
                                + "\r\n" + f1path + "\r\n" + '\r' + f2path + "\r\n")


# Remove any characters that google translator inserts that causes errors in subtitle files
def rm_err_chars(hd):
    t = hd.replace(' ->', ' -->')
    t = t.replace(' >', '->')
    t = t.replace(': ', ':')
    t = t.replace(' :', ':')
    t = t.replace(',', '.')
    return t

# Replace alphabetized numbers "eleven" with "11" and "thirty" with "30" that google translator creates
def replace_eleven_and_thirty(text):
    text = text.replace('eleven', '11')
    text = text.replace('thirty', '30')
    text = text.replace('0.', '0')  # New addition, removes "." that Google sometimes puts at the end of numbers
    text = text.replace('1.', '1')
    text = text.replace('2.', '2')
    text = text.replace('3.', '3')
    text = text.replace('4.', '4')
    text = text.replace('5.', '5')
    text = text.replace('6.', '6')
    text = text.replace('7.', '7')
    text = text.replace('8.', '8')
    text = text.replace('9.', '9')
    text = text.replace('6th', '6')
    text = text.replace('7th', '7')
    return text


# increment the number at the end  of the file name so can load next file in sequence
# Returns the file name  with the number in it incremented by one
def inc_filename(filename):
    num_str = filename[-6:-4]
    num1 = int(num_str)
    num1 += 1
    if num1 < 10:
        str_num1 = '0' + str(num1)
        return filename.replace(num_str, str_num1)
    else:
        return filename.replace(num_str, str(num1))


def check_file_name_for_number(filename):
    filename = filename.replace('.srt', "")
    filename = filename.replace('.txt', "")
    num_str = filename[-2:]
    if num_str.isnumeric():
        return True
    else:
        return False

def open_file(path):
    if os.path.exists(path):
        try:
            return codecs.open(path, encoding='utf-8', mode='r')
        except UnicodeEncodeError:
            message_not_UTF_8(path)
            return 0
    else:
        message_file_does_not_exist(path)
        return 0

def check_for_UTF_8(path):
    if len(path) < 0:
        return False
    try:
        enc = tokenize.open(path)
    except SyntaxError:
        return False
    result = str(enc.encoding)
    if result == 'utf-8-sig':
        return True
    else:
       return False
