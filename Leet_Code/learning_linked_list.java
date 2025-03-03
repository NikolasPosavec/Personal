// A linked list node
class ListNode 
{
    int data; //number
    ListNode next; //pointer

    // Constructor to initialize a new node with data
    ListNode(int new_data) 
    {
        this.data = new_data;
        this.next = null;
    }
}

public class learning_linked_list 
{

    // Function to traverse and print the singly linked list
    public static void traverseList(ListNode head) 
    {

        // A loop that runs till head is nullptr
        while (head != null) {

            // Printing data of current node
            System.out.print(head.data + " ");

            // Moving to the next node
            head = head.next;
        }
        System.out.println();
    }

    public static ListNode combine_lists(ListNode list1, ListNode list2) {
        // Create a dummy node to start the combined list
        ListNode combined_list = new ListNode(0);
        ListNode current = combined_list; // Pointer to build the list
    
        // Add all nodes from list1 to combined_list
        while (list1 != null) {
            current.next = new ListNode(list1.data); // Make a new node with list1's data
            current = current.next; // Move to the new node
            list1 = list1.next; // Go to the next node in list1
        }
    
        // Add all nodes from list2 to combined_list
        while (list2 != null) {
            current.next = new ListNode(list2.data); // Make a new node with list2's data
            current = current.next; // Move to the new node
            list2 = list2.next; // Go to the next node in list2
        }
    
        // Skip the dummy node to get the real head of the combined list
        combined_list = combined_list.next;
    
        // Count how many nodes are in the combined list
        int count = 0;
        ListNode temp = combined_list; // Temporary pointer to count nodes
        while (temp != null) {
            count++;
            temp = temp.next;
        }
    
        // Put all the data from the combined list into an array
        int[] arr_of_combd = new int[count];
        temp = combined_list; // Reset temp to the start of the list
        for (int i = 0; i < count; i++) {
            arr_of_combd[i] = temp.data; // Copy data into the array
            temp = temp.next;
        }
    
        // Sort the array using my forward and backward passes
        // Forward pass
        for (int i = 0; i < count - 1; i++) {
            if (arr_of_combd[i] > arr_of_combd[i + 1]) {
                int step = arr_of_combd[i + 1];
                arr_of_combd[i + 1] = arr_of_combd[i];
                arr_of_combd[i] = step;
            }
        }
        // Backward pass
        for (int i = count - 1; i > 0; i--) {
            if (arr_of_combd[i] < arr_of_combd[i - 1]) {
                int step = arr_of_combd[i];
                arr_of_combd[i] = arr_of_combd[i - 1];
                arr_of_combd[i - 1] = step;
            }
        }
    
        // Put the sorted data back into the combined list
        temp = combined_list; // Reset temp to the start of the list
        for (int i = 0; i < count; i++) {
            temp.data = arr_of_combd[i]; // Update the node's data
            temp = temp.next;
        }
    
        // Return the sorted combined list
        return combined_list;
    }

    
    public static void main(String[] args) 
    {
        //initialzing the lists
        ListNode head1 = new ListNode(1);
        head1.next = new ListNode(2);
        head1.next.next = new ListNode(4);

        ListNode head2 = new ListNode(1);
        head2.next = new ListNode(3);
        head2.next.next = new ListNode(4);
        
        combine_lists(head1, head2);

        /*printing the lists
        traverseList(head1);
        traverseList(head2);*/


    }
}
