# vacoompy

Simple file procesor scan file systems for files matching certain criteria and apply actions to them. 
Each rule is  a section in a ini style file ~/.vacoom/rules.ini : 

```ini
[Pdf in download folders]
directories: ['/Users/peter/Downloads']
extensions: ['pdf']
destination = /Users/peter/pdfs/
enabled = 1
action = move
```
All actions get logged in ~/.vacoom/vacoom.log

TODO

Extend criteria for matching and actions. 
