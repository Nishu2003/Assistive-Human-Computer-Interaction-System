import operator
import speech_recognition as s_r
import pyttsx3

print("Your speech_recognition version is: "+s_r.__version__)
r = s_r.Recognizer()
my_mic_device = s_r.Microphone(device_index=1)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

exit_phrase = "exit"

while True:
    with my_mic_device as source:
        print("Say what you want to calculate, or say 'exit' to end the program.")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    my_string = r.recognize_google(audio)
    print(my_string)

    if my_string.lower() == exit_phrase:
        speak("Exiting the program. Goodbye!")
        break

    def get_operator_fn(op):
        return {
            '+' : operator.add,
            '-' : operator.sub,
            'x' : operator.mul,
            'divided' : operator.truediv,
            'Mod' : operator.mod,
            'mod' : operator.mod,
            '^' : operator.xor,
        }[op]

    def eval_binary_expr(op1, oper, op2):
        op1, op2 = int(op1), int(op2)
        return get_operator_fn(oper)(op1, op2)

    result = eval_binary_expr(*(my_string.split()))
    print("Result:", result)
    speak("The result is " + str(result))
