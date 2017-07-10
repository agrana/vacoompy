# vacoompy
File procesor scan file systems for files matching certain criteria and apply actions to them. 
Each rule should be a section in a ini style file like this: 

[Pdf in download folders]
directories: ['/Users/peter/Downloads']
extensions: ['pdf']
destination = /Users/peter/pdfs/
enabled = 1
action = move

Extensions and directories are python lists inside de ini file. 
