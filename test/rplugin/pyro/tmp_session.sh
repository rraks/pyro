NVIM_LISTEN_ADDRESS=/tmp/nvim nvim test.txt -c "UpdateRemotePlugins | q " -u ./vimrc
NVIM_LISTEN_ADDRESS=/tmp/nvim nvim test.txt -c "let g:pyro_macro_path='$PWD/macros'" -u ./vimrc

