# Installation, this a plugin of ECY.
Required
> Plug 'hy172574895/EasyCompleteYou'

Use Plugin-manager
> Plug 'hy172574895/ECY-dictionary'

and then 

```
:ECYInstall dictionary
```

中国用户可以使用这个镜像，会快很多很多！
> Plug 'https://gitee.com/Jimmy_Huang/ECY-dictionary'

# Options
## g:dictionary_csv_file_path
**String**  
default value: '~/ecdict.csv'

## g:dictionary_show_chinese_in_preview_windows
**Boolean**  
default value: v:true  
To use Chinese in preview windows. To use English if its values is false.  
such as `let g:dictionary_show_chinese_in_preview_windows = v:false`  


## g:dictionary_additional_dict_path
**List**  
default value: []

Path to txt file you want, encodeing must be 'utf-8'.  
Such as `let g:dictionary_additional_dict_path = ['/home/example1/wordlist.txt']

# License
    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
        Version 2, December 2004

Copyright 2020 Jimmy Huang(1902161621@qq.com)

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.

# Acknowledgment
https://github.com/skywind3000/ECDICT
