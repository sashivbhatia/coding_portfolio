//Sashiv Bhatia
//May 3rd, 2023
//CSE 123
//Abosh Upadhyaya
//Repository

import java.util.*;

//This class builds and manages a repository that tracks a history of changes made to a program
public class Repository {
    private String name;
    private Commit head;

    public static class Commit {
        public final String id;
        public final String message;
        public Commit past;

        public Commit(String message, Commit past) {
            this.id = getNewId();
            this.message = message;
            this.past = past;
        }
    
        public Commit(String message) {
            this(message, null);
        }

        public String toString() {
            return id + ": " + message;
        }

        private static String getNewId() {
            return UUID.randomUUID().toString();
        }
    }

//This constructor creates a new repository with given name
//Takes one parameter: the name of the repository
//If given name is null or empty, throws an Illegal Argument Exception
    public Repository(String name){
        if(name==null || name==""){
            throw new IllegalArgumentException();
        }
        this.name=name;
    }

//This method returns the id of the latest commit
//Returns null if there have been no past commits
    public String getRepoHead(){
        if(this.head==null){
            return null;
        }
        return this.head.id;
    }

//Returns a string representation of the repository's name and the latest commit
//If there have been no past commits, returns the name of the repository with a message
//showing there have been no commits
    public String toString(){
        if(this.head==null){
            return this.name + " - No commits";
        }
        return this.name + " - Current head: " + this.head.toString();
    }

//This method checks if the repository contains a past commit with a given id
//Returns true if it contains a commit with that id, false if it doesn't or if there have been no past commits
    public boolean contains(String targetId){
        boolean check = false;
        Commit temp = head;
        while(temp!=null){
            if(temp.id.equals(targetId)){
                check=true;
            }
            temp=temp.past;
        }
        return check;
    }

//This methos returns a string representation of a given number of past commits 
//Takes one parameter: the number of commits in the history to show
//If the number given is non positive, throws an illegal argument Exception
//If the number given is larger than the number of past commits, it returns a string representation of all the past commits
//If there are no past commits, returns a blank string
    public String getHistory(int n){
        if(n<=0){
            throw new IllegalArgumentException();
        }
        String str = "";
        Commit temp = head;
        for(int i = 0; i<n && temp!=null; i++){
            if(i>0){
                str=str+"\n";
            }
            str = str + temp.id + ": " + temp.message;
            temp=temp.past;
        }
        return str;
    }

//This method creates a new latest commit with a unique id and a given message
//Takes one parameter:the message 
//Returns the id of the new commit
    public String commit (String message){
        head = new Commit(message, head);
        return this.head.id;
    }

//This method resets the repository by removing a given number of the past commits
//Takes one parameter:the number of commits to remove
//If the number is non positive, throws an illegal argument Exception
    public void reset(int n){
        if(n<=0){
            throw new IllegalArgumentException();
        }
        while(this.head!=null && n>0){
            this.head=this.head.past;
            n--;
        }
    }

//This method drops a commit with a given id
//Takes one parameter: the id to be checked for
//Returns true if the commit was successfully removed, false if not
//If there were no past commits, returns false
    public boolean drop(String targetId){
        boolean r = false;

        if(head!=null && head.id.equals(targetId)){
            head=head.past;
            r=true;
        }

        Commit temp = this.head;
        while(temp!=null && temp.past!=null){
            if(temp.past.id.equals(targetId)){
                temp.past=temp.past.past;
                r=true;
            }
            temp=temp.past;
        }
        return r;
    }

//This method squashes a commit with a given id with the commit before it and creates a new commit
//with a combined message and new id
//Takes one parameter: the id to be checked
//Returns true if the commits were sucessfully squashed, false if not
//Returns false if there were no past commits or if the targetId was not found in the history of commits

    public boolean squash(String targetId) {
        String m = "";
        Commit temp = head;
        Commit toSquash = null;
        Commit toSquash2 = null;

        if (temp == null) { 
            return false;
        }

        if (temp.id.equals(targetId)) { 
            if (temp.past == null) { 
                return false;
            }
            toSquash = temp;
            toSquash2 = temp.past;
            m = "SQUASHED: " + toSquash.message + "/" + toSquash2.message;
            Commit squashed = new Commit (m, temp.past.past);
            head = squashed;
            return true;
        }
        
        else{
            while (temp.past != null && temp.past.past != null) { 
                if(temp.past.id.equals(targetId)){
                    toSquash = temp.past;
                    toSquash2 = temp.past.past;
                    m = "SQUASHED: " + toSquash.message + "/" + toSquash2.message;
                    Commit squashed = new Commit(m, temp.past.past.past); 
                    temp.past = squashed;
                    return true;
                }
                temp = temp.past;        
            }
        }        
        return false;
    }
}
