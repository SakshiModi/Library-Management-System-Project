# Library-Management-System-Project

The library management system is built using Tkinter GUI toolkit. It is all about organizing, managing the library and library-oriented tasks. It also involves maintaining the database of entering new books and the record of books that have been issued and returned back to the library. The main aim of this project is providing an easy to handle and automated library management system. 



The following are some of the features provided by this project –

#### 1) Main Dashboard
Main Dashboard is the initial or the first window that opens at the very beginning. This window contains three buttons - Display Books, Employee, and Student. If this window is closed, all the running windows in the program closes.

#### 2) Display Books
Display Books button when pressed, opens a new window, displaying the Book ID, Book Name, and the Author Name. But if this button is located in the employee dashboard then it also displays the total quantity of books and the remaining quantity of books that is available for issue as shown below.

#### 3) Employee Login
The Employee button on the Main Dashboard opens a new window for Employee Login, i.e., the window contains two entry fields - Employee ID and Password. Moreover, there is a button to register if the employee is not a registered user.

#### 4) Employee Registration
The register button on Employee Login opens a new window for employee registration. When the employee is registered, a new window of Employee Dashboard is displayed. Moreover, the Employee Login window closes after one millisecond of clicking the register button.

#### 5) Employee Dashboard
Employee Dashboard opens after an employee logs in or registers on this application. This window contains five buttons – Display all Books, Lend/Return a Book, Fine Payment, Add a Book and Delete a Book.

#### 6) Employee Lend/Return a Book
When the Lend/Return a Book button on Employee Dashboard is pressed, a new window opens up asking for the Book ID and the Student's Roll No., so that the book could be issued or returned.

#### 7) Fine Payment
In the fine payment window, first the employee searches for the fine imposed on the student and accepts the money accordingly and updates it. This operation of updating the fine is performed only by the employee and so it’s a limitation that this feature is not automated.

#### 8) Add a Book
Add a book option adds a new book to the library if the name of the book and the author doesn't match the previous books. Also, it generates a Book ID on its own for the new book.

#### 9) Delete a Book
Delete a book option deletes old damaged or lost books from the library. This option helps to delete some or all the books from the library as per the requirement. It only requires the Book ID and the Quantity of Books to be entered.

#### 10) Student Login
The Student button on the Main Dashboard opens a new window for Student Login, i.e., the window contains two entry fields – Student Roll No. and Password. Moreover, there is a button to register if the student is not a registered user.

#### 11) Student Registration
The register button on Student Login opens a new window for student registration. When the student is registered, a new window of Student Dashboard is displayed. Moreover, the Student Login window closes after one millisecond of clicking the register button.

#### 12) Student Dashboard
Student Dashboard opens after a student logs in or registers on this application. This window contains three buttons – Display all Books, Lend/Return a Book and Issued Books.

#### 13) Student Lend/Return a Book
When the Lend/Return a Book button on Student Dashboard is pressed, a new window opens up asking for the Book ID, so that the book could be issued or returned by the students themselves.

#### 14) Issued Books
Issued Books button when pressed, opens a new window, displaying the book details with the issue, and the return date. Moreover, the fine amount is also displayed on that window. This window contains all the books that the particular student has issued so that the student can return them on time.
