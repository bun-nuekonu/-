# 誕生日ホルダー - Birthday holder
#### Video Demo:  <URL https://youtu.be/CN07wtzmMRU>
#### Description:
Birthday Holder is an application that allows you to register names and birthdays of yourself and others and manage the list in a list format.

This app has 11 functions:
1. login function
2. account registration function
3. add birthday function
4. Birthday List Display function
5. Display age and number of days until birthday function
6. Editing of added information function
7. Add a note function
8. Change your user name function
9. Delete all added birthdays function
10. Delete your account function
11. Logout function

##### 1. login function:
If you have already registered an account with this app, when you enter your username and password in the form, it will be checked against the information you have already registered, and if it matches, you will be able to access the app. If you enter a user name or password that is not registered with the app, a flash message will appear and the login will fail. Blank characters cannot be entered.

##### 2. account registration function:
If you have never registered an account with this app before, enter your username and password in the form, and re-enter your password for confirmation, and a new account will be created and you will be able to access the app. Blank characters cannot be entered.

##### 　3. add birthday function:
Clicking the "誕生日追加" button at the top of the top page will take you to a page where you can add your birthday and a form will appear. Enter the  name of the person you want to add, and the year, month, and day of birth, and your addition will be complete. Name, month and day of birth must be entered in the form.　Entering the year of birth is optional. You can also enter spaces in the name form, but do not use them except to separate names. Also, the maximum length of a name that can be registered is 10 characters.

##### 4. Birthday List Display function:
If you have registered more than one birthday, your name and birthday will be displayed on the top page in ascending date order. A "詳細" button will also appear along with the name and birthday.
If none of the birthdays have been registered, the name and birthday will not be displayed on the top page, but instead a statement will be displayed informing the user that the birthday has not been registered yet.

##### 5. Display age and number of days until birthday function:
Clicking the "詳細" button on the top page will take you to a page that displays detailed information associated with the registered name and birthday.
On the details page, you will see your name, birthday, age, number of days until your birthday, and a memo. The memo is not set at the beginning, but "ここにメモをいれてね" is displayed by default. At the bottom of the screen, there is an "編集" button and a "削除" button that allow you to edit the registered information or delete the information. For the displayed name, if you have not entered a year, the display of the age will be omitted.

##### 6. Editing of added information function:
Click the "編集" button at the bottom of the details page to display a form where you can edit the name and date of birth you have already registered. There is no need to enter new information from scratch, the form is pre-filled with the information you have already registered. If you have not registered a year, you can enter a new one, or conversely, you can delete a registered year. You can also add, edit, and delete notes here. You can enter up to 120 characters in the memo. If you delete all memos and press the "変更する" button when nothing is entered, a default sentence will be inserted. If you delete the name and press the Change button when nothing is entered, the name will not be changed.

#####　7. Add a note function:
The form at the bottom of the edit page allows you to add, edit, or delete memos. You can enter up to 120 characters in a memo. If you delete all memos and press the "変更する" button when nothing is entered, the default text will be inserted. You can also enter blank spaces and line breaks. If you make a line break, it will be reflected in the memo display on the detail page. This also allows you to bullet point your way through!

##### 8. Change your user name function:
Click the "設定" button in the upper left corner of the top page to go to the settings page. Click the "なまえを変える" button at the top of the settings page will take you to a page with a form where you can change your name. If you change your name here, the username of the account you are currently logged in as will be changed. When the change is complete, a flash message containing the new name will be displayed. Pressing the "変更する" button without changing the name in the form, or deleting the name and pressing the button with nothing entered, will cancel the name change. Blank characters cannot be entered.

##### 9. Delete all added birthdays function:
Click the "設定" button at the top left of the top page to go to the settings page. Click the "誕生日の全削除" button in the middle of the settings page to go to the page where you can confirm that you want to delete all the birthdays you have registered so far. There are two buttons on this page, and if you click the red "消す" button, all registered information including names and notes will be deleted at once. Once the data is deleted, it can't be undone! When the deletion is complete, you will be taken to the top page, where you can see that all the names and birthdays have disappeared. Press the green "やめる" button to cancel the batch deletion of birthdays and return to the settings screen. Please make your selection carefully.

##### 10. Delete your account function:
Click the "設定" button in the upper left corner of the top page to go to the settings page. Click on the red "アカウント削除" button at the bottom of the settings page to go to a page where you can confirm whether or not you want to delete the account you are currently logged into. There are two buttons on this page. Clicking on the red "消す" button will delete all the information you have registered, such as your name and notes, in one go, as well as all the data, including information about the currently logged-in account, such as username and password. Once the data has been deleted, it cannot be restored. Once the deletion is complete, you will be redirected to the login page. In order to log in, you need to register your account again on the registration page. Clicking the green "やめる" button will cancel the deletion of your account and return you to the settings page. Please make your selection carefully.

##### 11. Logout function:
Clicking the "ログアウト" button on the upper right corner of the top page will log you out of the account you are currently logged in to, and bring up the login page. To log in, you will need to enter your user name and password on the login page again.


Thank you for using this app. I hope this app will help you solve your problem!