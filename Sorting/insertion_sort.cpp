#include <iostream>
using namespace std;

void selection_sort(int arr[], int n)
{
    for(int i = 0; i<=n-1; i++){
        int j = i;
        while(j>0 && arr[j] < arr[j-1]){
            int temp = arr[j];
            arr[j] = arr[j-1];
            arr[j-1] = temp;
        }
        j--;
    }
   
}

void print_arr(int arr[], int size){
    for(int i = 0; i<size; i++){
        cout << arr[i] << " ";
    }
    cout<< endl;
}

int main()
{
    int arr[] = {1, 5332, 4, 13412, 5233213, 412325, 412312, 233123, 23123, 2423};
    
    int size = sizeof(arr)/sizeof(arr[0]);

    selection_sort(arr, size);

    cout << "Sorted array: ";
    print_arr(arr, size);
    return 0;
}  
