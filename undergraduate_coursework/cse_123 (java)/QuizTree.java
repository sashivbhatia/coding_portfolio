//Sashiv Bhatia
//May 24th, 2023
//CSE 123
//Abosh Upadhyaya
//QuizTree

import java.io.PrintStream;
import java.util.Scanner;

//This class allows the user to create a quiz tree, take the quiz 
//and to make edits such as adding questions
public class QuizTree {
    private QuizTreeNode root;

//This class represents a quiz tree node in the quiz 
    public static class QuizTreeNode {
        public String message;
        public QuizTreeNode left;
        public QuizTreeNode right;

//This constructor creates a quiz tree node with a given message
        public QuizTreeNode(String message){
            this.message = message;
        }
    }

//This constructor creates a quiz tree with a given quiz file
//Parameter: input file
    public QuizTree(Scanner inputFile) {
        this.root = constructTree(inputFile);
    }

//This method helps in creating a quiz with a given quiz file
//Parameter: the quiz file
//Returns: quiz tree node with the quiz constructed
    private QuizTreeNode constructTree(Scanner scanner) {
        if (!scanner.hasNextLine()) {
            return null;
        }

        String line = scanner.nextLine();
        QuizTreeNode node = new QuizTreeNode(line);

        if (line.startsWith("END:")) {
            return node;
        }

        node.left = constructTree(scanner);
        node.right = constructTree(scanner);

        return node;
    }

//This method takes the created quiz 
//Parameter: a scanner to take answers from the user
//No return
    public void takeQuiz(Scanner console) {
        takeQuizHelper(root, console);
    }

//This method is a helper method, helps in taking the quiz
//Parameters: a scanner to take answers and a node in the quiz tree
//No return
//Displays an error message if the user's answer is not one of the options
    private void takeQuizHelper(QuizTreeNode node, Scanner console) {
        if (node == null) {
            return;
        }

        if (node.message.substring(0,4).equals("END:")) {
            String result = node.message.substring(4);
            System.out.println("Your result is: " + result);
        }
        else{
            int temp = node.message.indexOf('/');
            String s1 = node.message.substring(0,temp);
            String s2 = node.message.substring(temp+1);
            System.out.print("Do you prefer " + s1 + " or " + s2 + "? ");
            String input = console.nextLine().trim().toLowerCase();

            if (input.equals(s1)) {
                takeQuizHelper(node.left, console);
            } else if (input.equals(s2)) {
                takeQuizHelper(node.right, console);
            } else {
                System.out.println("Invalid response; try again.");
                takeQuizHelper(node, console);
            }
        }
    }

//This method exports the quiz onto a given file
//Parameter: the file to be outputed onto
    public void export(PrintStream outputFile) {
        export(root, outputFile);
    }

//This method heps in exporting the quiz
//Parameters: the file to be outputted onto and the current quiz node
//NO return
    private void export(QuizTreeNode node, PrintStream outputFile) {
        if (node == null) {
            return;
        }

        outputFile.println(node.message);

        if (!node.message.substring(0,4).equals("END:")) {
            export(node.left, outputFile);
            export(node.right, outputFile);
        }
    }

//This method adds a question to the quiz tree in place of an answer
//Parameters: the answer to be replaced, the left and right choices instead and the respective 
//answers for those choices
    public void addQuestion(String toReplace, String leftChoice, String rightChoice,
                            String leftResult, String rightResult) {
        addQuestion(root, toReplace, leftChoice, rightChoice, leftResult, rightResult);
    }

//This method helps add a question to the quiz tree in place of an answer
//Parameters: the answer to be replaced, the left and right choices instead, the respective 
//answers for those choices and the current quiz node
    private void addQuestion(QuizTreeNode node, String toReplace, String leftChoice, String rightChoice,
                               String leftResult, String rightResult) {
        if (node == null) {
            return;
        }

        if (node.message.substring(0,4).equals("END:") && node.message.equalsIgnoreCase("END:"+toReplace)) {
            node.message = leftChoice + "/" + rightChoice;
            node.left = new QuizTreeNode("END:" + leftResult);
            node.right = new QuizTreeNode("END:" + rightResult);
        } else {
            addQuestion(node.left, toReplace, leftChoice, rightChoice, leftResult, rightResult);
            addQuestion(node.right, toReplace, leftChoice, rightChoice, leftResult, rightResult);
        }
    }
}
