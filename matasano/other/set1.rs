# This was compiled against a very old version of rust
# Currently very unlikely to compile

extern crate serialize;


use std::num::{ToStrRadix, from_str_radix};
use std::iter::{range_step};
use std::ascii::{AsciiCast, IntoBytes};
use std::io::{File, BufferedReader};

use serialize::base64::{FromBase64, ToBase64, STANDARD};

static SCORES: &'static [f64] =  &[8.167, 1.492, 2.782, 4.253, 13.0, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 
				 						  0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074];


struct ByteString {
	vec: Vec<u8>
}

impl ByteString {
	fn to_b64(&self) -> String{
		//The table to convert values
		let result = self.vec.as_slice().to_base64(STANDARD);
		result.to_string()
	}

	fn from_b64<'a>(inp: &'a str) -> ByteString{
		let result = inp.from_base64();
		ByteString{vec: result.ok().unwrap()}
	}

	fn to_hex(&self) -> String{
		let mut res = String::new();

		for byte in self.vec.iter(){
			res = res.append(byte.to_str_radix(16).as_slice());
		}
		return res;
	}

	fn from_hex<'a>(inp: &'a str) -> ByteString {
		let mut res: Vec<u8> = Vec::new();

		for idx in range_step(0, inp.len(), 2){
			let bytes = inp.slice(idx, idx+2); //The two bytes we'll deal with
			let optional: Option<u8> = from_str_radix(bytes, 16);
			match optional {
				Some(_) => (),
				None => continue
			};
			res.push(optional.unwrap());
		}
		return ByteString{vec: res};
	}

	fn to_ascii(&self) -> String{
		let ascii_xord = self.vec.as_slice().to_ascii();
		return ascii_xord.as_str_ascii().to_string()
	}

	fn from_ascii<'a>(inp: &'a str) -> ByteString{
		let to_vec = Vec::from_slice(inp.to_ascii());
		return ByteString{vec: to_vec.into_bytes()};
	}

	fn xor_eq(&self, other: ByteString) -> ByteString{
		//Zip it so we can easily using iterators to map ov`er
		let zipped = self.vec.iter().zip(other.vec.iter());
		//Apply xor to the zipped vector
		let mapped = zipped.map(|(&x, &y)| {x ^ y}).collect();

		return ByteString{vec: mapped};
	}

	fn xor_single(&self, other: u8) -> ByteString{
		let xord: Vec<u8> = self.vec.iter().map(|&x| x ^ other).collect();
		return ByteString{vec: xord};
	}

	fn xor_repeating(&self, other: ByteString) -> ByteString{
		let substr = other.vec;
		let mut collected: Vec<u8> = Vec::new();
		let mut counter = 0;

		while collected.len() < self.vec.len(){
			let gotten = substr.get(counter);
			collected.push(*gotten);
			counter += 1;
			if counter == substr.len(){
				counter = 0;
			}
		}
		return self.xor_eq(ByteString{vec: collected});
	}
		
}


fn score(inp: &str) -> f64 {
	//Scores from a-z
	let scores: Vec<f64> = Vec::from_slice(SCORES);
	//Convert all to lower so we only need deal with one case
	let ascii = inp.to_ascii().to_lower();
	let mut glob_score: f64 = 0f64;
	//ascii lowercase begins at 97, and if a character isn't in the range 97 to 122 then we ignore it
	for val in ascii.iter(){
		let idx = val.to_byte();

		if idx == 32 {
			//Got to consider spaces as without considering them the score can be boosted quite a bit towards random chars
			glob_score += 6.57;
		}
		else if idx >= 97 && idx <= 122{
			let index = (idx - 97) as uint;
			glob_score += *scores.get(index);
		}
	}
	return glob_score;
}

fn hamming<'a>(first: &'a [u8], second: &'a [u8]) -> uint {
	let mut sum = 0;
	for (&x, &y) in first.iter().zip(second.iter()){
		if x != y {sum += 1}
	}
	sum

}

fn detect_best_sxor(res: ByteString) -> (f64, u8, String) {
	let mut maximumChar = 0;
	let mut maximumScore = 0.0;
	let mut maximumString = String::new();

	for each in range(0u8, 128u8){
		//iterate over each possible ascii char from 0 to 128
		let xord: Vec<u8> = res.xor_single(each).vec;
		let ascii_xord = xord.as_slice().to_ascii();
		let xord_score = score(ascii_xord.as_str_ascii());
		if xord_score > maximumScore {
			maximumScore = xord_score;
			maximumChar = each;
			maximumString = ascii_xord.as_str_ascii().to_string();
		}
	}
	(maximumScore, maximumChar, maximumString)
}

fn detect_best_rxor(keysize: uint, res: ByteString) -> (f64, String, String) {
	//Assume we know the keysize length
	let length = (res.vec.len()/keysize) + 1;
	//This is a storage of vectors so we can get the result at the end
	let mut finalised: Vec<ByteString> = Vec::from_fn(length, |idx| ByteString{vec: Vec::new()});
	let mut key: ByteString = ByteString{vec: Vec::new()};
	let mut score: f64 = 0f64;
	//We break into blocks of length keysize
	//and then transpose
	//unfortunately that's difficult in rust atmo without a proper linalg
	//library.
	for sindex in range(0, keysize){
		let mut intermediate: Vec<u8> = Vec::new();
		//now we have an intermediate vector 
		//This contains the transposed block
		for idx_step in range_step(sindex, res.vec.len(), keysize){
			intermediate.push(*res.vec.get(idx_step));
		}
		let (s_score, character, string) = detect_best_sxor(ByteString{vec: intermediate});
		//better add the key so we get that at the end
		//Also sum up the score just for reference sake
		score += s_score;
		key.vec.push(character);
		//At this point we need to undo the transpose
		for (idx, val) in string.into_bytes().iter().enumerate(){
			finalised.get_mut(idx).vec.push(*val);
		}
	}
	let to_str_vec: Vec<String> = finalised.iter().map(|x| x.to_ascii()).collect();
	let key_finalised = key.to_ascii();
	(score, key_finalised, to_str_vec.concat())
}

fn detect_key_rxor(encoded: ByteString) -> (f64, String, String) {
	//If we want to detect a key assuming that key is in the range 2 to 40
	let (mut b_score, mut b_key, mut b_string) = (0f64, String::new(), String::new());
	for keysize in range(2, 40){
		let block1 = encoded.vec.slice(0, keysize);
		let block2 = encoded.vec.slice(keysize, keysize*2);
		let hamming_res = hamming(block1, block2) as f64/ keysize as f64;
		if hamming_res < 1f64{
			let (score, key, string) = detect_best_rxor(keysize, encoded.clone());
			if score > b_score{
				b_score = score;
				b_key = key;
				b_string = string;
			} 
		}
	}
	(b_score, b_key, b_string)
}


fn main(){
	matasano_six();
}

#[test]
fn test_hamming() {
	assert_eq!(3, hamming("kathrin".as_bytes(), "karolin".as_bytes()))
}

#[test]
fn matasano_one(){
	let b64 = ByteString::from_hex("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d").to_b64();
	assert_eq!(b64.as_slice(), "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t");
}


fn matasano_three(){
	let hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
	let (_, _, result) = detect_best_sxor(ByteString::from_hex(hex));
	println!("{0}", result);
	//assert_eq!(result.as_slice(), "Cooking MC's like a pound of bacon");
}


fn matasano_four() {
	//We're going to read in the file line by line
	let path = Path::new("Part4.txt");
	let mut file = BufferedReader::new(File::open(&path));

	//Mutable variables to hold the current maximum
	//Not confident enough with rust to do it over vectors
	//Functionally that'd be much nicer
	let mut maximumScore = 0.0;
	let mut maximumString = String::new();

	for line in file.lines(){
		//We need a strip function in the stdlib
		let mut unwrapped = line.ok().unwrap();
		if unwrapped.len() < 60 {continue}
		unwrapped.truncate(60);

		let bstring = ByteString::from_hex(unwrapped.as_slice());
		{
			//Here we check to see if it's a random string or not
			//If it contains any characters above 128 that implies it's not a string at all
			//We're only considering ascii
			let check_all_ascii: Vec<&u8> = bstring.vec.iter().filter(|&x| x < &128u8).collect();
			if check_all_ascii.len() < bstring.vec.len(){
				continue
			}
		}

		let (scr, _, strng) = detect_best_sxor(bstring);
		if scr > maximumScore {
			maximumScore = scr;
			maximumString = strng;
		}
	}
	println!("{0}", maximumString);
	//assert_eq!("Now that the party is jumping\n", maximumString.as_slice())
	//"Now that the party is jumping"
}


fn matasano_five() {
	let matasano = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal";
	let desired = "b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f";
	let bstring = ByteString::from_ascii(matasano);
	let encoder = ByteString::from_ascii("ICE") ;
	println!("{0}", bstring.xor_repeating(encoder).to_hex());
	//Note this does kinda work but there are a few errors, i.e. missing 0's.  Not sure why but it'd be because they didn't give
	//us a properly escaped string and all
	//assert_eq!(desired, bstring.xor_repeating(encoder).to_hex().as_slice());
}


fn matasano_six() {
	let path = &Path::new("Part6.txt");
	let mut file = BufferedReader::new(File::open(path));
	let mut collection = Vec::new();
	for line in file.lines(){
		let unwrapped = line.ok().unwrap();
		//unwrapped.pop_char();
		collection.push(unwrapped);
	}
	let finalised = ByteString::from_b64(collection.concat().as_slice());
	let (_, key, result) = detect_key_rxor(finalised);
	println!("KEY: {0}\nRESULT: {1}", key, result)
}

fn matasano_seven(){
	let path = &Path::new("Part7.txt");
	let mut file = BufferedReader::new(File::open(path));
	let mut collection = Vec::new();
	for line in file.lines(){
		collection.push(line.ok().unwrap());
	}
	let b_string = ByteString::from_b64(collection.concat().as_slice());
}
