from coderunner.runner import Runner

java_runner = Runner(language='java')
python_runner = Runner(language='python')

def test_java():
    result = java_runner.run("""
class Example {
    public static void main(String[] args) {
        System.out.println("Hello world from java!!!");
    }
}
    """)
    assert result['result'] == 'Hello world from java!!!\n'

def test_python():
    result = python_runner.run("print('Hello world from python!!!')")
    assert result['result'] == 'Hello world from python!!!\n'