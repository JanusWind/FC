# Lists all the git commands which are required to push the changes made.

c= None

git add --a
git commit -a
c = git commit -a
if ( c is None ) :
	continue
else :
	git push
