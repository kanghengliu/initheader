# Helper script for populating Yaml Header in Quarto Documents

This is my script for modifying/inserting yaml header in quarto documents. 

## Milestones:

* [X] Insert custom yaml header in quarto documents(**.ipynb, .qmd**)
* [X] Copy the quarto **`_extensions`** and CSS **`style`** folder to the target document directory
* [X] Detect whether there is origninal header in documents and prompt to replace.
* [X] Support for multiple quarto documents in one folder
* [ ] Auto update the quarto extensions when copying

## How to use:

1. ```shell
   git clone https://github.com/kanghengliu/initheader.git
   ```
2. browse quarto extensions u want to use, then copy to **`_extensions`** folder
3. put your favourite css/scss file into **`style`** folder
4. Edit yaml header to your liking in `init_header.py` ***NOTE: There are two header chunks that needs editing! One for ipynb and one for qmd!***
5. in terminal, run

   ```shell
   /Path/to/init_header.py "TITLE" "SUBTITLE" 1[0,False,True] /Path/to/doc[/Path/to/folder]
   ```
6. For help, run

   ```shell
   /Path/to/init_header.py -h
   ```
7. (Optional) Add script to .zshrc alias(MacOS/Linux) for quicker access
