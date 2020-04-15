from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
from flanker.addresslib import address
import sys
import getopt
import string
import pandas as pd

def ValidateEmails(sEmails,sOutputFile,bMX=False,bVerbose=False):
    bFile=False;
    if len(sOutputFile)>0:
        fOut=open(sOutputFile,"w")
        bFile=True;
    iCnt=0;
    for sEmail in sEmails:
        iCnt=iCnt+1;
        try:
            print("\r%i" % (iCnt));
            sOutputLine="";
            sEmail_1="";
            # email_validator
            try:
                v = validate_email(sEmail) # validate and get info
                sEmail_1 = v["email"] # replace with normalized form
            except EmailNotValidError as e:
                sEmail_1= "";
            # is_email
            try:
                if is_email(sEmail, check_dns=True):
                    sEmail_2=sEmail;
                else:
                    sEmail_2="";
            except:
                sEmail_2= "";
            # flanker
            try:
                sEmail_3="";
                if bMX:
                    sEmail_3=address.validate_address(sEmail).address;
                else:
                    sEmail_3=address.parse(sEmail).address;
                if sEmail_3 is None:
                    sEmail_3="";
            except:
                sEmail_3= "";
            # Resultado
            if bVerbose:
                print('Procesando: %s - 1: %s - 2: %s - 3: %s' % (sEmail, sEmail_1, sEmail_2, sEmail_3));
            sOutputLine=sEmail + '|' + sEmail_1 + '|' + sEmail_2 + '|' + sEmail_3 + '\n'; 
            if len(sOutputFile)>0:
                #print(sOutputLine);
                fOut.write(sOutputLine);
            else:
                print(sOutputLine);
        except Exception as e:
            sEmail="";
            print(e);
    if len(sOutputFile)>0:
        fOut.close()
    return;

def ReadContent(sFile, sDelimiter='\n',bVerbose=False):
    # read data
    ContentTxt = pd.read_csv(sFile,delimiter=sDelimiter,names=["EMAIL"], encoding='utf-8');
    ContentTxt = ContentTxt.dropna();
    ContentTxt = ContentTxt.drop_duplicates();
    return ContentTxt;

def main():
    bVerbose=False;
    bSuccess=True;
    bMX=False;
    UsageString= '--- AnalyseEmails.py ---\r\n';
    UsageString += '\t[-h] (Optional) Show this help message and exit\r\n';
    UsageString += '\t-i <Input file - one line for one email>\r\n';
    UsageString += '\t[-m] (Optional) Validate MX records (takes time)\r\n';
    UsageString += '\t[-o] <Output file> (Optional) One line for one email\r\n';
    UsageString += '\t[-v] (Optional) Verbose output\r\n';
    sInputFile = '';
    sOutputFile = '';
	# Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:vm",["ifile=","ofile="]);
    except getopt.GetoptError:
        print(UsageString);
        print("");
        print('ERROR: Unable to process command line parameters');
        bSuccess=False;
    for opt, arg in opts:
        if opt == '-h':
            print(UsageString);
            sys.exit(1);
        elif opt == "-v":
            bVerbose = True;
        elif opt == "-m":
            bMX = True;
        elif opt in ("-i", "--ifile"):
            sInputFile = arg;
        elif opt in ("-o", "--ofile"):
            sOutputFile = arg;
    if len(sInputFile)<=0:
        print(UsageString);
        print("");
        print('ERROR: Missing input file (-i / --ifile=)');
        bSuccess=False;

    if bSuccess:
        try:
            # read data
            print("Reading input file ",sInputFile);
            Emails_df = ReadContent(sInputFile,'\n',bVerbose);
            print('%i lines to be processed' % len(Emails_df));
            ValidateEmails(Emails_df["EMAIL"],sOutputFile,bMX,bVerbose);
            #reviews_df["review_clean"] = reviews_df["REVIEWS"].apply(lambda x: clean_text(x,sLanguage,bVerbose));
        except Exception as e:
            print("");
            print('ERROR: Error processing input');
            print(str(e));
            bSuccess=False;
    return bSuccess;


if __name__ == '__main__':
    bMainResult=main()
    if not bMainResult:
        exit(-1);
