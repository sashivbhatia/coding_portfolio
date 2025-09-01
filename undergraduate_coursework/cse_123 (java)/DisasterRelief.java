//Sashiv Bhatia
//May 3rd, 2023
//CSE 123
//Abosh Upadhyaya
//Disaster Relief
//This class is a program to figure out how to distribute a budget during a disaster
//to help the most amount of people.

import java.util.*;

public class Client {
    private static Random rand = new Random();

    public static void main(String[] args) throws Exception {
        // List<Location> scenario = createRandomScenario(10, 10, 100, 1000, 100000);
        List<Location> scenario = createSimpleScenario();
        System.out.println(scenario);
        
        double budget = 2000;
        Allocation allocation = allocateRelief(budget, scenario);
        printResult(allocation, budget);
    }

    //This method returns the allocation of budget that helps the most people.
    //If there is a tie in most people helped, it returns the allocation that costs the least
    //Parameters: the budget to be allocated and the list of locations
    //Returns: the ideal allocation of budget
    public static Allocation allocateRelief(double budget, List<Location> sites) {
        Set<Allocation> allocations = new HashSet<>();
        allocations.add(new Allocation());
        return allocateRelief(budget, sites, allocations, new Allocation());
    }

    //This method returns the allocation within a given budget that helps the most people and costs the least
    //Parameters: the budget to be allocated, the list of locations, a set of allocations and an allocation
    //Returns: the allocation that helps the most people with the least amount of budget spent

    private static Allocation allocateRelief(double budget, List<Location> sites, Set<Allocation> allocations, Allocation allo){
        Allocation temp = allo;
        for(int i = 0; i< sites.size(); i++){
            Location loc = sites.get(i);
            if((budget-allo.totalCost()-loc.getCost()>=0)&&(!allo.getLocations().contains(loc))){
                allocations.add(allo.withLoc(loc));
                temp = allo;
                allocateRelief(budget,sites,allocations,allo.withLoc(loc));
                temp = getBest(allocations);
            }
            sites.remove(i);
            sites.add(i, loc);
        }
        return temp;
    }

    //This method takes a set of possible ways to allocate the budget and returns the allocation that helps
    //the most people while spending the least budget
    //Parameters: the set of possible ways to allocate the budget
    //Returns: the best allocation that helps the most people while spending the least budget
    private static Allocation getBest(Set<Allocation> allocations){
        int max = -1;
        Allocation best = new Allocation();
        for(Allocation allo : allocations){
            if(max == allo.totalPeople() && best.totalCost()>allo.totalCost()){
                best=allo;
            } else if(max < allo.totalPeople()) {
                max = allo.totalPeople();
                best=allo;
            }
        }
        return best;
    }
    // PROVIDED HELPER METHODS - **DO NOT MODIFY ANYTHING BELOW THIS LINE!**

    public static void printResult(Allocation alloc, double budget) {
        System.out.println("Result: ");
        System.out.println("  " + alloc);
        System.out.println("  People helped: " + alloc.totalPeople());
        System.out.printf("  Cost: $%.2f\n", alloc.totalCost());
        System.out.printf("  Unused budget: $%.2f\n", (budget - alloc.totalCost()));
    }

    public static List<Location> createRandomScenario(int numLocs, int minPop, int maxPop, double minCostPer, double maxCostPer) {
        List<Location> result = new ArrayList<>();

        for (int i = 0; i < numLocs; i++) {
            int pop = rand.nextInt(minPop, maxPop + 1);
            double cost = rand.nextDouble(minCostPer, maxCostPer) * pop;
            result.add(new Location("Location #" + i, pop, round2(cost)));
        }

        return result;
    }

    public static List<Location> createSimpleScenario() {
        List<Location> result = new ArrayList<>();

        result.add(new Location("Location #1", 50, 500));
        result.add(new Location("Location #2", 100, 700));
        result.add(new Location("Location #3", 60, 1000));
        result.add(new Location("Location #4", 20, 1000));
        result.add(new Location("Location #5", 200, 900));

        return result;
    }    

    private static double round2(double num) {
        return Math.round(num * 100) / 100.0;
    }
}
