#include <iostream>
using namespace std;

void selection_sort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        int min = i;
        for (int j = i+1; j < n; j++)
        {
            if (arr[min] > arr[j])
            {
                min = j;
            }
        }
        if (i != min)
        {
            swap(arr[min], arr[i]);
        }
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

    cout << "Sorted array: " << endl;
    print_arr(arr, size);
    return 0;
}
