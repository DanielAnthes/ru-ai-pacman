import os, re, glob, shutil, subprocess, sys, getopt, pickle
from keyboard import keyboard
import pacman
import imp

solutionModule='competitionAgents'
solutionFile  =solutionModule + '.py'
execList=['-p', 'MyPacmanAgent', '-q', '-t', '--frameTime', '0', '-f', '-n', '10']
studentRegexp=r'_([^_]*)_.*'
logfileName = 'output.txt'
htmlstyle = 'leaderboard.css'
htmloutputfile = 'leaderboard.md'

def saveobject(filename,obj):
  #print("Saving ",obj)
  #print("to %s\n" % filename)
  output = open(filename, 'wb')
  pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def loadobject(filename):
  input = open(filename,'rb');
  obj=pickle.load(input)
  return obj

def getGroupName(file):
   m = re.search(studentRegexp, file)
   if m==None:
      m = re.search(studentRegexp[1:], file[file.find('/')+1:])
   return m.group(1) if not m==None else None

def gamesStats(games):
   scores = [game.state.getScore() for game in games]
   timeouts = [game.state.getTimeout() for game in games]
   moves  = [game.numMoves for game in games]
   times  = [games[i].totalAgentTimes[0]/float(moves[i]) if float(moves[i]) > 0 else 0 for i in range(len(games))]
   wins = [game.state.isWin() for game in games]
   winRate = wins.count(True)/ float(len(wins))
   avescore = sum(scores) / float(len(scores))
   return (scores,timeouts,moves,times,wins,winRate,avescore)

with open('userlist') as f:
   nameLookupDict = {line.split()[0]:line.split()[1].split('@')[0] for line in f.readlines()}

def nameLookup(snum):
   if snum in nameLookupDict:
      return nameLookupDict[snum]
   else:
      return snum

def generateHtml(filename,games, name=None):
   if name == None:
     name='Unnamed'     
   with open(filename) as f:
      content = f.read()
   snums = re.findall('s\d{7}',content)
   if len(snums) == 0:
      snums = [name]
   names = [nameLookup(snum) for snum in snums]
   namestr = ', '.join(names)
   if type(games[0]) is list :
      scores = []; timeouts=[]; moves=[]; times=[]; wins=[]; winRate=[]; avescore=[];
      for laygames in games: # average the per-layout averages
         (lscores,ltimeouts,lmoves,ltimes,lwins,lwinRate,lavescore)=gamesStats(laygames)
         scores.append(   sum(lscores)  /float(len(lscores))   )
         timeouts.append( sum(ltimeouts)/float(len(ltimeouts)) )
         moves.append(    sum(lmoves)   /float(len(lmoves))    )
         times.append(    sum(ltimes)   /float(len(ltimes))    )
         wins.append(     sum(lwins)    /float(len(lwins))     )
         avescore.append(lavescore)
      avescore = sum(avescore) / float(len(avescore))
   else:
      (scores,timeouts,moves,times,wins,winRate,avescore)=gamesStats(games)
	
   levels = zip(scores,wins,timeouts,moves,times)
   
   htmlout = ''
   htmlout += '{} | {:.0f} | Score | '.format(namestr,round(avescore))
   htmlout += ' | '.join(['{}'.format(score) for score in scores]) + '\n'
   htmlout += ' | | Win/Timeout | '
   htmlout += ' | '.join(['{:.1f}/{:.1f}'.format(win,timeout) for win,timeout in zip(wins,timeouts)]) + '\n'
   htmlout += ' | | Moves | '
   htmlout += ' | '.join(['{}'.format(move) for move in moves]) + '\n'
   htmlout += ' | | Move Time | '
   htmlout += ' | '.join(['{:.3f}'.format(time) for time in times]) + '\n'
   return (avescore,htmlout)

def runFile(file,replay=False,args=[]):
  fileoutput = ''
  # Fetch student number
  print(file)
  studentNumber = getGroupName(file)
  if studentNumber is None: studentNumber=''
  studentNumber=studentNumber.replace('20',' ')
  print('Trying ' + studentNumber) 
  fileoutput += studentNumber + ':' + '\n'
  #keyboard()

  
  # Move their competitionAgents.py to the environment
  try: 
    shutil.copy(file,solutionFile)
  except: 
    pass

  # Run the environment
  output = ''
  failed = False
  try:
    print('Trying ' + studentNumber)
    # force reload of student code -- needed even for load to get the class definitions correctly
    try:
       imp.reload(sys.modules[solutionModule]) 
    except Exception as e:
       print(e)
       return (0,'')
    if os.path.isfile('../saved/' + file + '_games.pk') and not replay:
      games = loadobject('../saved/' + file + '_games.pk')
    else:
      games = pacman.cmdlineRunGames(execList + args)
      saveobject('../saved/' + file + '_games.pk',games) # save so don't have to re-run later
    
    score,htmlsummary = generateHtml(file,games,studentNumber)    

  except subprocess.CalledProcessError as e:
    failed = True
    output = e.output
  # Print(result)
  if failed:
    fileoutput += 'Failed :\n' + output + '\n\n'
  else:
    fileoutput += 'Output :\n' + output + '\n\n'
  return (score,htmlsummary)

def help():
   return """Usage: ./{filename} [-h | --help --dir --num] [directory] [studentNumber]

This script copies the search.py and searchAgents.py pairwise from the given directory and executes pacman.py with all 12 configurations to test the search algorithms. 
The output is dumped into output.txt.
If this script runs with the studentNumber argument, it will only run search.py and searchAgents.py of that one student.
If no studentNumber argument is given, it will run all pairs of search.py and searchAgents.py.

-h|--help\t\tDisplays this help text.
--dir=[directory]\tSets the default directory with student solutions to the entered one. By default it is `{defaultDir}`.
--num=[studentNumber]\tScript will only execute search.py and searchAgents.py from this student.

Examples:
./{filename}\t\t\tRuns all file pairs in {defaultDir}/
./{filename} --dir=solutions\tRuns all file pairs in solutions/
./{filename} --num=s4050614\t\tRuns the file pair in {defaultDir}/ of the student 4050614
""".format(filename=__file__, defaultDir='studentsolutions')

def main(argv):
  defaultDirectory = 'studentsolutions'
  studentNumber = None
  replay=False
  logfile = open(logfileName,'w');

  # Parse the arguments
  try:
     opts, args = getopt.getopt(argv, 'h', ['help', 'dir=', 'num=', 'replay'])
  except getopt.GetoptError:
    opts=[]
    args=[]
    _, e, _ = sys.exc_info()
    if e.msg.find('not recognized')<0: # pass through unrecog optoins
       print((help()))
       sys.exit(2)

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print((help()))
      sys.exit()
    elif opt == '--dir':
       defaultDirectory = arg
    elif opt == '--num':
       studentNumber = arg
    elif opt == '--replay':
       replay = True
       
  # Remove the old fileoutput file
  if os.path.isfile('output.txt'):
     try:
       os.remove('output.txt')
     except:
       pass
   
  fileoutput = ''

  if not os.path.isdir(defaultDirectory):
    print(("Error : could not find directory :", defaultDirectory))
    exit(2)
  
  info=list()
  if studentNumber is None:
    # If you want to run them all at once
    solnfiles = sorted(glob.glob(defaultDirectory + '/*' + solutionFile))
    # extract student number and remove duplicates
    oldgroup=None
    files=[]
    #print('\n'.join(solnfiles))
    for file in solnfiles:
      groupName = getGroupName(file)
      if not groupName == None :
        if groupName == oldgroup:
          files[-1]=file
        else:
          oldgroup = groupName
          files.append(file)
    #print('\n'.join(files))
    for file in files:
      score,output = runFile(file,replay,args)
      logfile.write(output)
      info.append((score,output))
  else:
    # If you want to run one at the time using the student number
    for file in glob.glob(defaultDirectory + '/*' + solutionFile):
      groupName = getGroupName(file)
      if studentNumber == groupName or ( groupName is None and studentNumber=='' ):
        score,output = runFile(file,replay,args)
    logfile.write(output)
    info.append((score,output))

  # sort the results based on score
  info = sorted(info,reverse=True)
  # shutil.copy(htmlstyle,htmloutputfile) # copy in style info

  help_str = 'If your group is not listed, be sure to: hand in the assignment on Blackboard; hand in just competitionAgents.py and not a zip file; not add any strange import statements. If you think something is wrong, get in contact.\n\nPrint statements slow your agent down. Be sure to remove/comment all print statements before submitting your agent.\n\nAre not all group member names shown? Be sure to include a comment with all s-numbers in the code.\n\nNotice your score fluctuating between versions of the leaderboard? This is because the average is not very strong: each level is only run 10 times. For the final leaderboard, each level will be run 50 times, so the average will be more precise.\n\nHighscores previous years\n\n| 2014 | 2015 | 2016 |\n|---|---|\n| 2195 | 2243 | 2279 |\n\n'

  with open(htmloutputfile,'w') as hfile:
    # write the header
    hfile.write(help_str+'\n\n')
    hfile.write("Group | Avg Score | Info/Level ")
    hfile.write(''.join(["| %d " % i for i in range(12)]))
    hfile.write('\n')
    for _ in range(15):
      hfile.write('| --- ')
    hfile.write('\n')
    for score,output in info:
      hfile.write(output)
  return info

if __name__ == "__main__":
  # make back up of current solution file, if it's not already there!
  if not os.path.isfile(solutionFile+".orig"):
    shutil.copy(solutionFile,solutionFile + ".orig")  
  try:
    __import__(solutionModule)
  except: # current solutinFile is broken, copy back the .orig 
    print("Warning: " + solutionFile + " is broken!  reverting to " + solutionFile + ".orig")
    print("     your broken file is saved to : " + solutionFile + ".bak")
    shutil.copy(solutionFile,solutionFile + ".bak") # restore backup    
    shutil.copy(solutionFile + ".orig",solutionFile) # restore backup
    __import__(solutionModule)
    
  # ask for arguments if none given
  if len(sys.argv) == 1:
      sys.argv.extend([x for x in re.split(r' *',input("Enter any command line arguments?")) if x!=''])
  main(sys.argv[1:])
