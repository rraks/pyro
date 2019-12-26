![PyRo](https://github.com/rraks/webmedia/blob/master/pyro/pyro.png "PyRo")
A neovim interface to write simple list manipulating python snippets. 

## Demo
![](https://github.com/rraks/webmedia/blob/master/pyro/pyro.gif)

## Usage
- Hit `:Pyro` or `:Pyro/ga` to open a pyro editor on a new tab with all lines of the previous buffer passed as input arguments to the snippet.
- Edit the snippet and hit :w to *save* and render a preview on the scratch buffer to the left.
- *Save* the scratch buffer to reflect the output back to the original buffer in append mode (appends after line).
- Go back to original buffer by either closing this tab ` :tabclose` or `:gt`.
- Hit `:Pyro/gr` to do the same action as show in the gif but replace the lines in the original buffer.
- Hit `:Pyro/<pattern>/r` to do the same only for the lines containing required pattern but **replace** the line in the input buffer.
- Hit `:Pyro/<pattern>/a` to do the same only for the lines containing required pattern but **append** below the line in the input buffer.
- Macros are stored in the `pyro_macro_path` set in vimrc. You may quickly open a previously used python snippet by hitting `:e! ./` and select the macro.
- Macros can be saved with a custom name `:w new_file_name` and can be opened for later use.


## Installation
Set the macro save path  
` let g:pyro_macro_path="path/to/macro/save/folder" `  
Ensure you have set the python3_host_prog to the python environment where pynvim is installed.  
` let g:python3_host_prog = 'python3/host/prog/path' `  

### Using vim-plug  
`Plug 'rraks/pyro'`  
From inside neovim  
` :UpdateRemotePlugins `  

### From Github
Clone this repo and add it to your rtp path.  
` let &runtimepath.=',path/to/this/git/repository/root' `  
From inside neovim  
` :UpdateRemotePlugins `  

## Tests
A test vimrc and session startup script is provided in the test/rplugin/pyro folder.  
This is mandatory to run all the test scripts.  
```
cd test/rplugin/pyro
./tmp_session.sh
```
All tests of the test folder are to be run from the root folder  
For example -  
`python test/rplugin/pyro/pyrotest.py SimpleTests.pyro_simple `
