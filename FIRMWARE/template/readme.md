the template folder in this directory can be used for doing pico firmware. 
Don't change this version of the folder, just copy it and use it as a template for your own project.
Refer to the directions below for how to use it.

Using c for the pico:

https://www.youtube.com/watch?v=i8MqFmR0W3E

use this as a template repo: git clone https://github.com/LearnEmbeddedSystems/rp2040-project-template.git

open it in vscode but open it with the pico short cut, use pico arm gcc kit

edit cmakelists to include whatever libraries you want for the code you're gonna do

also use cmakelists to change the name of the output file

when ready to run the code, go to the cmake tab and build the project

now the output uf2 file will be in the build folder. now just flash it onto the pico