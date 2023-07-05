import numpy as np
import cv2
from collections import Counter


def main():

    # INSERT image pathway: Test image:
    image = cv2.imread('testimage.jpg')

    # Convert the image into an array:
    numpy_array = np.array(image)

    # Reshapes the array so that it has the shape
    # (n, 3), with one column, n rows, and 3 terms/tuple:
    reshaped_array = numpy_array.reshape(-1, 3)

    # tuple(row) converts each row of the reshaped_array into a tuple
    # 'for row' assigns each element in reshaped_array to 'row'.
    # This converts the reshaped array into a list of tuples:
    tuple_list = [tuple(row) for row in reshaped_array]

    # Counts the frequency of the tuples:
    tuple_counts = Counter(tuple_list)

    # Prompts the user to give the number of objects in segmentation:
    n = int(input("Enter the number of objects in segmented image (excluding the background color): ")) + 1

    # Finds the n most common tuples, since the most frequent color values should be
    # those used to segment the image:
    hfreq_tuples = tuple_counts.most_common(n)
    print("\nIntended segmentation colors:")
    for tpl, count in hfreq_tuples:
        print(f"Tuple: {tpl}, Frequency: {count}")

        # Inserts a clear division between the intended and unintended segmentation colors:
        print("\n------------------------------")

    # Gives the remaining tuples with the lower frequencies, since these should be
    # those not intended to exist within the segmented image:
    lfreq_tuples = [tpl for tpl in tuple_counts if tpl not in dict(hfreq_tuples)]
    if lfreq_tuples:

        print("\nUnintended segmentation colors:")
        for tpl in lfreq_tuples:
            count = tuple_counts[tpl]

            # Inserts a clear division between the different tuples and their iterations/surrounding tuples:
            print("\n------------------------------")

            # Prints the tuple and their frequencies:
            print(f"\nTuple: {tpl}, Frequency: {count}")

            # idx is a list that contains the indices tuple_list items that are equal to tpl:
            idx = [i for i, t in enumerate(tuple_list) if t == tpl]

            # Continues to run check of term i if it matches the above requirement:
            for iter_index, i in enumerate(idx):

                # Returns the array as a tuple, removing the last element of the tuples
                # as they give the number of color channels while we are looking for the
                # row and column indices:
                row_idx, col_idx = np.unravel_index(i, numpy_array.shape[:-1])

                # Creates an empty list of the surrounding tuples:
                surrounding_tuples = []

                # Prints the tuple to which the surrounding tuples are associated to,
                # along with its iteration:
                print(f"\nIteration {iter_index + 1}:")
                print(f"Row Index: {row_idx}")
                print(f"Column Index: {col_idx}")
                retrieved_tuple = numpy_array[row_idx, col_idx]
                # flat_index = np.ravel_multi_index((row_idx, col_idx), numpy_array.shape[:-1])
                # print(f"Index: {flat_index}")

                # Creates an iterative loop from row_idx-1 to, but excluding, row_idx+2:
                for r in range(row_idx - 1, row_idx + 2):

                    # This is indented since we want the index to be within the
                    # correct rows and columns, creating a 3x3 search area around a tuple:
                    for c in range(col_idx - 1, col_idx + 2):

                        # Note that shape[0] gives the 0-index element of tuples, which gives the rows,
                        # and shape[1] gives the 1-index element of the tuples, which gives the columns:
                        if (0 <= r < numpy_array.shape[0] and
                                0 <= c < numpy_array.shape[1]):

                            # Removes the tuple itself from the list of the surrounding tuples:
                            if tuple(numpy_array[r, c]) != tpl:
                                # Appends these surrounding tuples to the surrounding_tuples list:
                                surrounding_tuples.append(tuple(numpy_array[r, c]))

                # Prints a list of surrounding tuples under each iteration:
                print(surrounding_tuples)

                obj_list = [("error")]
                count_list = [0]

                # Iterate over the indexes of hfreq_tuples
                for i, (tpl, _) in enumerate(hfreq_tuples):

                    # Initialize a counter for the current index
                    counter = Counter()

                    # Iterate over the surrounding tuples
                    for surrounding_tuple in surrounding_tuples:
                        if surrounding_tuple == tpl:
                            counter[surrounding_tuple] += 1

                    # Print the counts for the current index
                    for obj, count in counter.items():
                        print(f"Frequency of {obj}: {count}")
                        obj_list.append(obj)
                        count_list.append(count)
                print(obj_list, count_list)
                # try saving obj to obj_list and count to count_list. Find largest item in count list, then determine its index
                # its corresponding object in the obj_list should give with obj is most frequent.
                max_count = max(count_list)
                print(max_count)
                max_index = count_list.index(max_count)
                print(max_index)
                max_obj = obj_list[max_index]
                print(max_obj)
                # print(numpy_array[flat_index])
                print(retrieved_tuple)
                if max_obj != 'error':
                    numpy_array[row_idx, col_idx] = max_obj
                else:
                    print("No correct surrounding colors")
                print(numpy_array[row_idx, col_idx])
        print(numpy_array)

        # Convert the modified numpy_array back to an image
        output_image = np.uint8(numpy_array)

        # INSERT file name: Save the image to a file
        output_filename = 'output_image.jpg'  # Choose a filename and extension for the output image
        cv2.imwrite(output_filename, output_image)

        # Display a message indicating the image has been saved
        print(f"The modified image has been saved as {output_filename}")

        # Eventually make it so that the loop runs, re-evaluating unintended
        # tuples until there are none left.

        # Makes things look grainy...instead make it easier for them to manually choose
        # what color value to switch it to?

        # Add way to prompt user for upload file pathname and saved file name

    else:
        print("\nNo unintended segmentation colors.")

if __name__ == '__main__':
    main()
