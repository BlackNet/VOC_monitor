# update to current level
git pull

# add changes
git add .

# today please
current_date=$(date +"%Y-%m-%d %T")

# start commit
echo "description of this push"
read desc

git commit -m "$desc from ${current_date}" -m "${m1}" -m "${m2}" -m "${m3}" -m "${m4}"

# dump it
git push
  