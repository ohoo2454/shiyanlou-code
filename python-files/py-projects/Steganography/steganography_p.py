import sys
from PIL import Image


def make_even_image(image):
	pixels = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1, a >> 1 << 1)
			for r, g, b, a in image.getdata()]
	even_image = Image.new(image.mode, image.size)
	even_image.putdata(pixels)
	return even_image


def encode_data_in_image(image, data):
	even_image = make_even_image(image)
	int_to_binary_str = lambda i: '0' * (8 - len(bin(i)[2:])) + bin(i)[2:]
	binary = ''.join(map(int_to_binary_str, bytearray(data, 'utf-8')))
	if len(binary) > len(even_image.getdata()) * 4:
		raise Exception("Error: Can't encode more than " + 
				len(even_image.getdata()) * 4 + " bits in this image. ")
	encoded_pixels = [(r + int(binary[index * 4 + 0]),
					   g + int(binary[index * 4 + 1]),
					   b + int(binary[index * 4 + 2]),
					   t + int(binary[index * 4 + 3]))
			if index * 4 < len(binary) else (r, g, b, t)
			for index, (r, g, b, t) in enumerate(even_image.getdata())]
	encoded_image = Image.new(even_image.mode, even_image.size)
	encoded_image.putdata(encoded_pixels)
	return encoded_image


def decode_data_from_image(image):
	binary = ''.join([bin(r)[-1] + bin(g)[-1] + bin(b)[-1] + bin(a)[-1]
			for r, g, b, a in image.getdata()])
	many_zero_index = binary.find('0' * 16)
	end_index = (many_zero_index + 8 - many_zero_index % 8
			if many_zero_index % 8 != 0 else many_zero_index)
	data = binary_to_string(binary[:end_index])
	return data


def binary_to_string(binary):
	index = 0
	strings = []

	def effective_binary(binary_part, zero_index):
		if not zero_index:
			return binary_part[1:]
		binary_list = []
		for i in range(zero_index):
			small_part = binary_part[8 * i: 8 * i + 8]
			binary_list.append(small_part[small_part.find('0') + 1:])
		return ''.join(binary_list)

	while index + 1 < len(binary):
		zero_index = binary[index:].index('0')
		length = zero_index * 8 if zero_index else 8
		string = chr(int(effective_binary(
				binary[index: index + length], zero_index), 2))
		strings.append(string)
		index += length
	return ''.join(strings)


def main():
	image_file, new_image_file = sys.argv[1:]
	image = Image.open(image_file)
	str_to_hide = 'Hello World!'
	new_image = encode_data_in_image(image, str_to_hide)
	new_image.save(new_image_file)
	print(decode_data_from_image(new_image))


if __name__ == '__main__':
	main()
	